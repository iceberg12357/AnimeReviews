from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models import user
from flask_app.models.anime import Anime
from flask import flash

genre = ["Action","Adventure","Comedy","Drama","Fantasy","Isekai","Music","Romance","Scifi","Seinen",
"Shojo","Shonen","Sports","Supernatural","Thriller"]

@app.route('/anime/<int:id>')
def anime(id):
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data = {
        "id": id
    }
    userr = {
        "id": session['user_id']
    }
    print(session['user_id'])
    oneUser = user.User.getOne(userr)
    anime = Anime.getAnime(data)
    return render_template('displayReview.html', anime=anime, currentUser=oneUser)

@app.route('/anime/new')
def newAnime():
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    userr = {
        "id": session['user_id']
    }
    genres = genre
    print(session['user_id'])
    oneUser = user.User.getOne(userr)
    return render_template('newReview.html', currentUser=oneUser, genres=genres)

@app.route('/createAnime', methods=["POST"])
def createAnime():
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    if not Anime.animeValidation(request.form):
        return redirect('/anime/new')
    data = {
        'user_id': session['user_id'],
        'title' : request.form['title'],
        'creator' : request.form['creator'],
        'year' : request.form['year'],
        'platform' : request.form['platform'],
        'genre' : request.form['genre'],
        'thoughts' : request.form['thoughts'],
    }
    print(session['user_id'])
    anime = Anime.save(data)
    print(anime, "heading - to - save")
    return redirect('/home')

@app.route('/anime/edit/<int:id>')
def editAnime(id):
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data = {
        "id": id
    }
    userr = {
        "id": session['user_id']
    }
    genres = genre
    print(session['user_id'])
    oneUser = user.User.getOne(userr)
    anime = Anime.getAnime(data)
    return render_template('editReview.html', anime=anime, currentUser=oneUser, genres=genres)

@app.route('/updateAnime', methods=["POST"])
def updateAnime():
    Anime.update(request.form)
    return redirect('/home')
    
@app.route('/anime/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data ={
        'id': id
    }
    print(data)
    Anime.delete(data)
    return redirect('/home')
