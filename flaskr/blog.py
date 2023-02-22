from itertools import zip_longest

import click
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# 'blog' corresponds to the Blueprint's name
# '__name__' helps locate the root path of the Blueprint
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Show all the posts and their corresponding information, most recent first."""
    db = get_db()

    posts = db.execute(
        'SELECT p.id, title, body, created, p.author_id, username, cnt.post_id_sum'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' LEFT OUTER JOIN'
        '  (SELECT post_id, COUNT(*) AS post_id_sum FROM upvote GROUP BY post_id) cnt'
        '  ON p.id = cnt.post_id'
        ' ORDER BY created DESC;'
    ).fetchall()
    upvoted_posts = get_upvoted_posts()

    post_info = zip_longest(posts, upvoted_posts, fillvalue=0)
    return render_template('blog/index.html', post_info=post_info)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?);',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(post_id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param post_id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author"""
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?;',
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


def get_upvoted_posts():
    """Gets a list of all posts that the current user has upvoted.

    :return: list of all upvoted posts by the current user"""
    db = get_db()
    is_logged_in = hasattr(g.user, 'id')

    upvoted_posts = [] if not is_logged_in else db.execute(
        'SELECT p.id, EXISTS(SELECT upvoter_id, post_id'
        '  FROM upvote u'
        '  WHERE u.post_id = p.id AND u.upvoter_id = ?) AS is_upvoted'
        ' FROM post p'
        ' ORDER BY p.id DESC;',
        (g.user['id'],)
    ).fetchall()

    u = db.execute(
        'SELECT p.id, EXISTS(SELECT upvoter_id, post_id'
        '  FROM upvote u'
        '  WHERE u.post_id = p.id AND u.upvoter_id = ?) AS is_upvoted'
        ' FROM post p'
        ' ORDER BY p.id DESC;',
        (g.user['id'],)
    ).fetchall()
    click.echo(u[1]['is_upvoted'])
    return upvoted_posts


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    """Update a post if the current user is the author."""
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?;',
                (title, body, post_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    """Delete a post.

    Ensures that the post exists and that the logged-in user is the
    author of the post."""
    get_post(post_id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?;', (post_id,))
    db.execute('DELETE FROM upvote WHERE post_id = ?;', (post_id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/like', methods=('POST',))
@login_required
def upvote_post(post_id):
    """Increments the upvote counter for a post by 1 if its upvote button is selected.

    Only decrements the upvote counter for that post by 1 if its Upvote Button was
    previously selected AND is deselected."""
    get_post(post_id)
    db = get_db()

    db.execute('DELETE FROM post WHERE id = ?;', (post_id,))
    db.execute('DELETE FROM upvote WHERE post_id = ?;', (post_id,))
    db.commit()

    return redirect(url_for('blog.index'))
