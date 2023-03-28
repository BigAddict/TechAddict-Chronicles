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

Use the following credentials to test the website without creating an account.

- Email: guest@tomar.com
- Password: guest

<!-- ABOUT THE PROJECT -->
## About The Project

[![Screenshot](static/images/home-page.png?raw=true "Tomar")](https://tomar.up.railway.app/)


## Features
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

### Installation

1. Clone the repo and navigate to ```tomar``` directory
   ```
   git clone https://github.com/balewgize/tomar.git
   ```
   ```
   cd tomar
   ```
2. Install required packages (virtual environments recommended)
   ```
   python3 -m venv venv && source venv/bin/activate
   ```
   ```
   pip install -r requirements/local.txt
   ```
3. Provide credentials in *.env* (example in .env.dev file)
   ```
    DJANGO_SECRET_KEY=
   ```
   Use the following command to generate random *SECRET_KEY*
   ```
   python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
4. Run tests (each app can also be tested individually)
   ```
   python manage.py test
   ```
5. Apply migrations and start the server
    ```
    python manage.py migrate
    ```
    ```
    python manage.py runserver
    ```
6. Goto http://127.0.0.1:8000 on your browser.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

Thanks!
