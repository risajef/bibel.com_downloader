# bibel.com_downloader
Python script to download whole bible from bible.com

```
podman build . -t bibleanalytics
podman run --mount source=./ destination=/app/ bibleanalytics
```


Create migration from start:
```
rm database/database.db
rm -r database/migrations/versions/*
CTRL+p -> '>' -> 'Debug: Start without debugging'
CTRL+p -> '>' -> 'Tasks: Run Task' -> 'Alembic autogenerate migrations'
CTRL+p -> '>' -> 'Tasks: Run Task' -> 'Alembic migrate'
```