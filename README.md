# Nextcloud mail attachment push service

This repository provides a small python application that fetches mails
from a given IMAP account and pushes the attachment to a Nextcloud.

## Getting started

### Running it with 🐳 Docker

The application can be run easily with a single docker command. 
Please prepare a `.env` file in the format of `.env.sample`.

```bash
docker run --env-file .env samuelspagl/nextcloud-mail-attachment-push
```

### Running the python script

This project is build upon `pipenv`.

```bash
pipenv install --dev
```

```bash
pipenv shell
export $(xargs < .env) 
python main.py
```

## Contributions

Are always welcome. In my head I'm still figuring out what to add, but if you have
suggestions, just hit me up.
