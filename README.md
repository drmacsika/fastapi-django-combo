# FastAPI and Django Combo
This projects aims to combine FastAPI and Django to build a Production ready application capable of utilizing all of the features of both django and FastAPI.
To demonstrate, I built a sample blog app, It can be adapted into any app.

Table of Contents:
- [Screenshots](#screenshots)
- [Tools](#tools)
- [Features](#features)
- [Installation and Usage](#installation)
- [Contributing](#contributing)
- [Additional Info](#additional-info)


## Screenshots

![Django Admin Page 1](https://github.com/drmacsika/fastapi-django-combo/blob/master/templates/Screenshot%202021-10-23%20at%2023.12.52.png)

![Django Admin Page 2](https://github.com/drmacsika/fastapi-django-combo/blob/master/templates/Screenshot%202021-10-23%20at%2023.13.05.png)

![Fastapi Blog endpoints 1](https://github.com/drmacsika/fastapi-django-combo/blob/master/templates/Screenshot%202021-10-23%20at%2023.13.42.png)

![Fastapi Blog endpoints 2](https://github.com/drmacsika/fastapi-django-combo/blob/master/templates/Screenshot%202021-10-23%20at%2023.13.51.png)


## Tools

- Django
- Django Rest Framework (DRF)
- FastAPI
- Pydantic with custom validation
- Django all-auth
- JWT Authentication
- CORS
- Uvicorn and Gunicorn for Python web server

## Features

- CRUD endpoints for blog posts and categories
- CRUD endpoints for contacts
- Asynchronous CRUD endpoints for user accounts
- Endpoints for user authentication using DRF
- Django settings file
- Migrations using Django Migrations
- Django ORM and Admin Page
- JWT token authentication.

## Installation and Usage

Use the package manager [pip](https://pip.pypa.io/en/stable/) for installation.

```bash
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- cd fastapi-django-combo
- python manage.py makemigrations
- python manage.py migrate
- uvicorn core.asgi:app --reload
```

## Contributing

Pull requests and contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

Ensure to follow the [guidelines](https://github.com/drmacsika/fastapi-django-combo/blob/master/CONTRIBUTING.md) and update tests as appropriate.


## Additional Info

For an in-depth understanding of FastAPI or any of the tools used here including questions and collaborations, you can reach out to me.
