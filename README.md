# FastAPI and Django Combo
This projects aims to combine FastAPI and Django to build a Production ready application capable of utilizing all of the features of both django and FastAPI.
To demonstrate, I built a sample blog app, It can be adapted into any app.

## Table of Contents:
- [Screenshots](#screenshots)
- [Tools](#tools)
- [Features](#features)
- [Installation and Usage](#installation)
- [Tutorial](#tutorial)
- [Contributing](#contributing)
- [Contact Info](#contact-info)

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
- python manage.py collectstatic
- python manage.py createsuperuser
- uvicorn core.asgi:app --reload
```

## Tutorial:
- **Tutorial 1**: *[How to use FastAPI with Django ORM and Admin](https://nsikakimoh.com/learn/django-and-fastapi-combo-tutorials)*

## Contributing

Pull requests and contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

Ensure to follow the [guidelines](https://github.com/drmacsika/fastapi-django-combo/blob/master/CONTRIBUTING.md) and update tests as appropriate.

## Contact Info
If you have any question or want to reach me directly, 
[Contact Nsikak Imoh](https://nsikakimoh.com).

