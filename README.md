# Software engineering & agile assignment
For the Software engineering And Agile assignment I have created a help desk where users can raise different types of issues which can then be reviewed by administrators. As specified in the brief, admins have full CRUD while users can only read,write and update. For privacy and security, users can only view their own issues they have raised while admins can view all issues and delete them if needed.

## installation
to run the application a few third party packages need to be installed, run the command bellow in the root directory:

```bash
pip install -r requirements.txt
```
Alternatively you can install the packages manually by running:
> [!WARNING]
> It is highly recommended to install via the requirements.txt file 
```bash
pip install fastapi jinja2 uvicorn sqlalchemy httpx pytest
```

## Running the application
> [!CAUTION]
> This application requires Python 3.11+, it is highly suggested to use Python 3.12.4

to run a local instance of the application you can run the following command in the root of the project:

```bash
uvicorn app.main:app --reload
```
## Deployed application
> [!CAUTION]
> The application may cold start and take a few minutes to be accessible due to the limitations of the free plan on the provider.

The application is deployed on: https://sea-assignment-help-desk.onrender.com/register

## testing

to run the unit tests run the following command in the root of the project:

```bash
pytest
```

## Why I chose FastAPI

## entity relationship diagram

## mockups

## Custom authentication process


## Jinja2 inheritance

## Project structure

## ci/cd



