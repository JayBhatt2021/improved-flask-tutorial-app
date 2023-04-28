# Flaskr

Flaskr (sometimes referred to as the "Improved Flask Tutorial App" in the project) is an improved version of
**The Pallet Projects**' [official Flask tutorial](https://github.com/pallets/flask/tree/2.2.4/examples/tutorial). In
addition to its original features (registering/logging-in users, creating posts, etc.), this version of Flaskr also
allows users to upvote (like) posts. However, the code in this repository differs greatly from the one in the official
tutorial as it heavily uses Flask-Login and Flask-SQLAlchemy.

## Installation

First, `git clone` this repository, and navigate to the `flask-tutorial` directory.

```bash
$ git clone https://github.com/JayBhatt2021/improved-flask-tutorial-app.git
$ cd flask-tutorial
```

If you use **macOS/Linux**, use the following commands to create your virtual environment folder and activate it,
respectively:

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Otherwise, input these commands on the **Windows** Command Prompt:

```bash
$ py -3 -m venv .venv
$ .venv\Scripts\activate
```

Now, install Flaskr and its dependencies.

```bash
$ pip install -e .
```

## Usage

Use Waitress to run the application.

```bash
$ waitress-serve --host 127.0.0.1 --port 8336 --call flaskr:create_app
```

Open http://127.0.0.1:8336 in the browser.
