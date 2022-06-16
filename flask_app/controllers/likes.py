from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models import user
from flask_app.models.like import Like
from flask import flash

@app.route('/user/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data ={
        'anime_id': id,
        'user_id': session['user_id']
    }
    if Like.isLiked(data):
        return redirect('/home')
    Like.save(data)
    return redirect('/home')

    

@app.route('/user/unlike/<int:id>')
def unlike(id):
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data ={
        'anime_id': id,
        'user_id': session['user_id']
    }
    Like.unlike(data)
    return redirect('/home')

