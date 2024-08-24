# SEA-assignment

## installation
to run the application a few third party packages need to be installed, run the command bellow to run them:

```bash
pip install fastapi jinja2 uvicorn sqlalchemy httpx
```

## Running the application

to run a local instance of the application you can run the following command in the root of the project:

```bash
uvicorn app.main:app --reload
```

## testing

to run the unit tests run the following command in the root of the project:

```bash
pytest
```