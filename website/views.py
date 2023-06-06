"""
To store standard routes.
We need to register the blueprint in __init__.py
To render the home.html template we have imported render_template
"""
# from flask import Blueprint

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# Whenever user visits the base url or home.
# The home function will be called.
@views.route('/', methods=['GET', 'POST'])
# Only access the home page if logged in
@login_required
def home():
    # return "<h1>Test</h1>"

    if request.method == 'POST':
        note = request.form.get('note')

        # To check if the note body length is more than one.
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Add the note to the database.
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    # To render home.html
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
