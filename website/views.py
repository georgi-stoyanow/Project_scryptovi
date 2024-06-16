from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        method = request.form.get('_method', 'POST')
        if method == 'POST':
            note = request.form.get('note')
            if len(note) < 1:
                flash('Note is too short!', category='error') 
            else:
                new_note = Note(data=note, user_id=current_user.id) 
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        elif method == 'PATCH':
            note_id = request.form.get('note_id')
            return update_note_internal(note_id)
        elif method == 'DELETE':
            note_id = request.form.get('note_id')
            return delete_note_internal(note_id)
    
    return render_template("home.html", user=current_user)

def update_note_internal(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        new_data = request.form.get('note')
        if len(new_data) < 1:
            flash('Note is too short!', category='error')
        else:
            note.data = new_data
            db.session.commit()
            flash('Note updated!', category='success')
    else:
        flash('Note not found or unauthorized', category='error')
    return redirect(url_for('views.home'))

def delete_note_internal(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', category='success')
    else:
        flash('Note not found or unauthorized', category='error')
    return redirect(url_for('views.home'))
