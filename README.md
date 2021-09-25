# Hackernews

## Latest update

Changed the algorithm used in fetching the stories from the [API][1]. Instead of getting only the new (latest) stories, I now get the maximum or largest (latest) item ID, then walk backwards to fetch subsequent ones:

```python
...

def get_max_item_id():
    max_item_id = requests.get(f"{BASE_API_URL}/maxitem.json")
    return max_item_id.json()

@shared_task
def store_latest_stories():
    max_item_id = get_max_item_id()
    for sid in reversed(range(max_item_id)):
        story_response = get_item(sid)
        ...
```

Also, the UI now allows only the item types available in the database for filtering. As soon as a new item type is included, it will automatically be added to the filters.

## Update

**It is live on heroku at [newhackernews.herokuapp.com][0].**

This application tends to make it easier to navigate Hackernews by utilizing its public [API][1]. It provides a better UX and interativity courtesy its real-time searching and filtering capabilities, beautiful UI, and lazy-loading. Custom API was also incorporated for ease of accessibility, though [POST requests][2] require [token-based authentication][3]. Though it depends on hackernews API, all the available data are stored in a separate database and hosted on this platform thereby providing parallel storage and preventing a single source of failure. Hence more reliable. It looks like:

![Home page of the application](home.png "Home page of the application")

![Detail page of each story in the application](detail.png "Detail page of each story in the application")

Data are being consumed every 5 minutes via a background task powered by [Celery][4] with [redis][5] as the broker. This presents performance gains as users do not need to wait for such actions' completions.

The application also provides an in-depth text searching with search term highlighting. Though it is not an enterprise grade full-text search functionality but it is close to that. PostgreSQL could have been used as database to fascilitate full-text search but it was later dropped during development. It ended up being used in production.

## Local setup

The application was built on a Linux machine (Pop!\_OS 20.04 LTS) with [Python][6] 3.8.10, [git][8], and [redis][5] installed. Virtual environment was managed by [pipenv][7] though you can opt for other virtual environment tools (`requirements.txt` is included). Ensure your machine has all these tools to locally run this web application.

A typical setup to the app up and running locally is stated below:

-   Get the program source files: You can clone it from Github via:
    ```bash
    git clone https://github.com/Sirneij/Hackernews.git
    ```
-   Change directory into the source code folder:
    ```bash
    cd Hackernews
    ```
-   Activate virtual environment ([pipenv][7] is used here but you can use virtualenv, venv, poetry, or conda):
    ```bash
    pipenv shell
    ```
-   Install the web application's dependencies (again, [pipenv][7] is used here but you are at liberty to use any other tool. `requirements.txt` is included):
    ```bash
    pipenv install
    ```
-   Create migrations (migrations folder already populated. If you prefer to start afresh, delete all the files in the `migrations` folder of each major app &mdash; `accounts`, and `news` &mdash; except the `__init__.py` files. Then, in your terminal, execute `python manage.py makemigrations`):

    ```bash
    python manage.py migrate
    ```

-   You can opt to create super user by executing:

    ```bash
    python manage.py createsuperuser
    ```

    Provide the details requested by the prompts that follow.

-   Run the application. You will need a second terminal to start the [Celery][4] tasks. In one terminal, start the application:

    ```bash
    python manage.py runserver
    ```

    You can **optionally** provide a port as the default port is `8000`. To provide a port, the command above becomes:

    ```bash
    python manage.py runserver port_number
    ```

    You can now visit your browser and navigate to `http://localhost:8000/` or `http://localhost:port_number/` as the case may be.

    In the second terminal, start the celery tasks by (ensure your virtual environment is activated):

    ```bash
    celery -A hackernews worker -l info -B
    ```

## About the Web application

The application was built using [Django web framework][9], [Tailwind CSS][16], [SQLite][10] database and [redis][5] as a broker for [celery][4]. It has the following structure:

```bash
.
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── celerybeat-schedule
├── db.sqlite3
├── detail.png
├── hackernews
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── settings
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── __init__.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── home.png
├── manage.py
├── news
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_comment_story.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tasks.py
│   ├── templatetags
│   │   ├── custom_tags.py
│   │   └── __init__.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── Pipfile
├── Pipfile.lock
├── Procfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── runtime.txt
├── setup.cfg
├── static
│   ├── admin
│   │   ├── css
│   │   │   ├── autocomplete.css
│   │   │   ├── ...
│   │   ├── fonts
│   │   │   ├── LICENSE.txt
│   │   │   ├── ...
│   │   ├── img
│   │   │   ├── calendar-icons.svg
│   │   │   ├── ...
│   │   └── js
│   │       ├── actions.js
│   │       ├── ...
│   ├── css
│   │   ├── all.min.css
│   │   ├── style.css
│   │   └── tailwind.min.css
│   ├── images
│   │   └── useravatar.png
│   ├── js
│   │   ├── jquery.min.js
│   │   ├── mark.min.js
│   │   └── scripts.js
│   └── webfonts
│       ├── fa-brands-400.eot
│       ├── ...
└── templates
    ├── base.html
    ├── includes
    │   └── _header.html
    └── news
        ├── comments.html
        ├── commons
        │   └── _filters.html
        ├── detail.html
        ├── index.html
        └── stories.html

32 directories, 210 files
```

The major apps are `news` and `accounts`. While the former handles almost all the physical functionalities of the system, the latter only does user stuff. The `api` app exposes the data for consumption. It is documented using [drf-yasg][11], a [Swagger][12] generation tool implemented without using the schema generation provided by Django Rest Framework. The `api` has a [token-based authentication][3] which requires that all [POST requests][2] must provide a `token` to be accepted, otherwise a not too interesting response:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

will be given. To get a token, you can use the following:

```bash
http POST http://127.0.0.1:8000/api/api-token-auth/ username=your_username password=your_password
```

Or in your terminal:

```bash
python manage.py drf_create_token user_name
```

If the user account is available, you should have a response like:

```json
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Fri, 24 Sep 2021 08:30:18 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.10
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "55868c9d71901f4bb09059eb0a669485511586f7"
}
```

or (for terminal):

```bash
Generated token 55868c9d71901f4bb09059eb0a669485511586f7 for user sirneij
```

You can then use the token for requests such as:

```bash
http POST http://localhost:8000/api/latest-stories/ 'Authorization: Token 55868c9d71901f4bb09059eb0a669485511586f7' title="Just testing" story_type="story" text="Just some text" dead=false story_url="http://localhost:8000/api/latest-stories/"
```

which should give you something like:

```json
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 399
Content-Type: application/json
Date: Fri, 24 Sep 2021 08:44:03 GMT
Location: http://localhost:8000/api/latest-stories/dd6fdcdd-da6f-45c8-a3bb-e883b5a16419/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.10
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "author": "sirneij",
    "created_by": "sirneij",
    "dead": false,
    "descendants": null,
    "id": "dd6fdcdd-da6f-45c8-a3bb-e883b5a16419",
    "score": 0,
    "slug": "just-testing",
    "story_type": "story",
    "story_url": "http://localhost:8000/api/latest-stories/",
    "text": "Just some text",
    "time": "2021-09-24T08:44:03.688895Z",
    "title": "Just testing",
    "url": "http://localhost:8000/api/latest-stories/dd6fdcdd-da6f-45c8-a3bb-e883b5a16419/"
}
```

If you need to make this request in a python application using the [requests][13] library, you can do something like:

```python
import requests

url = 'http://localhost:8000/api/latest-stories/'
payload = {

    "title": "Title of the story",
    "story_type": "story",
    "text": "some text",
    "dead": true,
    "story_url": "http://example.com"

}
headers = {'Authorization': 'Token 55868c9d71901f4bb09059eb0a669485511586f7'}
r = requests.post(url, headers=headers, data=payload)
```

You can achieve same with JavaScript's [fetch][14], or [axios][15].

That is pretty much it!!!

**You can connect with or follow me on [LinkedIn][17], and [contact me for a job, something worthwhile or buying a coffee ☕](mailto:sirneij@gmail.com)**

[0]: https://newhackernews.herokuapp.com/ "newhackernews.herokuapp.com"
[1]: https://hackernews.api-docs.io "Hackernews API"
[2]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST "POST"
[3]: https://www.okta.com/identity-101/what-is-token-based-authentication/ "What Is Token-Based Authentication?"
[4]: https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html "Using Celery with Django"
[5]: https://redis.io/ "Redis"
[6]: https://www.python.org/ "python.org"
[7]: http://manpages.ubuntu.com/manpages/impish/man1/pipenv.1.html "pipenv"
[8]: https://git-scm.com/downloads "Git"
[9]: https://www.djangoproject.com/ "Django"
[10]: https://www.sqlite.org/index.html "SQLite"
[11]: https://github.com/axnsan12/drf-yasg/ "drf-yasg"
[12]: https://swagger.io/ "Swagger"
[13]: https://docs.python-requests.org/en/latest/ "Python requests"
[14]: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch "Fetch API"
[15]: https://www.npmjs.com/package/axios "axios"
[16]: https://tailwindcss.com/ "Tailwind css"
[17]: https://www.linkedin.com/in/idogun-john-nelson/ "Idogun John Nelson"
