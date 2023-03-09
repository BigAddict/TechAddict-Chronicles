<a name="readme-top"></a>

<div align="center">
  <h3 align="center">Tomar</h3>

  <p align="center">
    Medium like website where users can read and share stories freely!
    <br />
    <a href="https://tomar.up.railway.app/" target="_blank"><strong>View Demo »</strong></a>
    <br />
  </p>
</div>

Use the following credentials to test the website without creating an account

- Email: guest@tomar.com
- Password: guest

<!-- ABOUT THE PROJECT -->
## About The Project

[![Screenshot](static/images/home-page.png?raw=true "Tomar")](https://tomar.up.railway.app/)


## Features
- Email verification
- Email only sign up
- Profile for users
- Bookmark and Like posts 
- Draft and Published posts
- CRUD posts with permission
- Bootstrap 5 for frontend
- Follower and Following 
- Search functionality
- Comment on posts
- Rich text editor (CKEditor)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
- Python/Django
- Bootstrap
- JavaScript/jQuery
- PostgreSQL
- Gunicorn
- Railway

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Django
* PostgreSQL
* SendGrid API key

### Installation

1. Clone the repo
   ```
   git clone https://github.com/balewgize/tomar.git
   ```
2. Install required packages
   ```
   pip install -r requirements.txt
   ```
3. Provide credentials in *.env*  (create a file named .env inside **tomar** folder - project root directory)
   ```
    DJANGO_SECRET_KEY=
    DJANGO_DEBUG=True

    DEFAULT_FROM_EMAIL=
    SENDGRID_USER=
    SENDGRID_API_KEY=

    PGDATABASE=
    PGUSER=
    PGPASSWORD=
    PGHOST=
    PGPORT=

    ADMIN_URL=
   ```
4. Apply migrations
    ```
    python manage.py migrate
    ```
5. Create super user and start the server
    ```
    python manage.py createsuperuser
    ```
    ```
    python manage.py runserver
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

Thanks!
