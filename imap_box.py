import os
import time
from io import BytesIO

import ulid
from imap_tools import AND, MailBox
from nc_py_api import Nextcloud
from rich import print

NEXTCLOUD_URL = os.environ.get("NEXTCLOUD_URL")
NEXTCLOUD_USER = os.environ.get("NEXTCLOUD_USER")
NEXTCLOUD_PASSWORD = os.environ.get("NEXTCLOUD_PASSWORD")
NEXTCLOUD_FOLDER_PATH = os.environ.get("NEXTCLOUD_FOLDER_PATH")

IMAP_SERVER = os.environ.get("IMAP_SERVER")
IMAP_USERNAME = os.environ.get("IMAP_USERNAME")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD")
IMAP_POLL_INTERVAL = int(os.environ.get("IMAP_POLL_INTERVAL", "10"))

APPEND_ULID_TO_FILENAME = int(os.environ.get("APPEND_ULID_TO_FILENAME", 1))
INITIAL_SCAN = int(os.environ.get("INITIAL_SCAN", 0))

nc_client: Nextcloud
imap_client: MailBox


def main():
    print(
        f"[CONFIG] Configuration values:\n"
        f" - NEXTCLOUD_URL: {NEXTCLOUD_URL}\n"
        f" - NEXTCLOUD_USER: {NEXTCLOUD_USER}\n"
        f" - NEXTCLOUD_PASSWORD: {NEXTCLOUD_PASSWORD}\n"
        f" - NEXTCLOUD_FOLDER_PATH: {NEXTCLOUD_FOLDER_PATH}\n"
        f" - IMAP_SERVER: {IMAP_SERVER}\n"
        f" - IMAP_USERNAME: {IMAP_USERNAME}\n"
        f" - IMAP_PASSWORD: {IMAP_PASSWORD}\n"
        f" - IMAP_POLL_INTERVAL: {IMAP_POLL_INTERVAL}\n"
        f" - INITIAL_SCAN: {INITIAL_SCAN}"
    )
    global nc_client
    nc_client = Nextcloud(
        nextcloud_url=NEXTCLOUD_URL,
        nc_auth_user=NEXTCLOUD_USER,
        nc_auth_pass=NEXTCLOUD_PASSWORD,
    )
    global imap_client
    imap_client = MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD)
    if INITIAL_SCAN == 1:
        print("[MAIN] Initial scan is set to true, starting to scan already read mails")
        fetch_and_push(True)
        print("[MAIN] Finished initial scan")
    while True:
        fetch_and_push()
        time.sleep(IMAP_POLL_INTERVAL)


def format_filename(filename: str):
    special_char_map = {ord("ä"): "ae", ord("ü"): "ue", ord("ö"): "oe", ord("ß"): "ss"}
    random_gen = ulid.ULID().generate()
    fl_name, file_extension = os.path.splitext(filename)
    return f"{fl_name.translate(special_char_map)}-{random_gen}{file_extension}".encode(
        "ascii", "ignore"
    ).decode("ascii")


def fetch_and_push(seen=False):
    for msg in imap_client.fetch(AND(seen=seen)):
        print(
            f"[INBOX] Found a new mail with the title '{msg.subject}' from '{msg.from_}' on the {msg.date}"
        )
        for atta in msg.attachments:
            print(f"> {atta.filename}")
            nc_client.files.upload_stream(
                f"{NEXTCLOUD_FOLDER_PATH}{format_filename(atta.filename)}",
                BytesIO(atta.payload),
            )


if __name__ == "__main__":
    main()
