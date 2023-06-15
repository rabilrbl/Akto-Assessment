# Periodic PII fetcher with cron

This is a simple script that fetches PII from a given URL and stores it in a mongo database. It is meant to be run periodically with cron.

## Usage

```bash
$ pip3 install -r requirements.txt
$ python3 script.py &
```

## Configuration

The script is configured with environment variables. The following variables are required:

- `MONGO_URI`: The URI of the mongo database to use.
- `MONGO_DB_NAME`: The name of the mongo database to use.
- `MONGO_COLLECTION_NAME`: The name of the mongo collection to use.
- `CRON_MINUTES`: The interval in minutes at which to run the script periodically.
