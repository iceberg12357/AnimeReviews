from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models import anime
from flask_app.models import like

from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def logUndReg():
    return render_template('logUndReg.html')

@app.route('/register', methods=["POST"])
def register():
    if not User.validateRegister(request.form):
        return redirect('/')
    encrypted_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "firstName": request.form['firstName'],
        "lastName": request.form['lastName'],
        "email": request.form['email'],
        "password": encrypted_pw,
    }
    user_id = User.createOne(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/login', methods=["POST"])
def login():
    data = {"email": request.form['email']}
    user_with_email = User.getByEmail(data)
    if user_with_email == False:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_with_email.id
    return redirect('/home')

@app.route('/home')
def mainPage():
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    print(session['user_id'])
    oneUser = User.getOne(data)
    animes = anime.Anime.getAllAnimes()
    for each in animes:
        info ={
            'anime_id': each.id,
            'user_id': session['user_id']
        }
        likes = like.Like.getAllLikes(info)
        print(likes)
        each.isLiked = like.Like.isLiked(info)
        print(each.isLiked)
        each.totalLikes = likes
    return render_template('main.html', currentUser=oneUser, animes=animes)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login or register to proceed")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    print(session['user_id'])
    oneUser = User.getOne(data)
    animes = anime.Anime.getAllAnimesByUser(data)
    for each in animes:
        info ={
            'anime_id': each.id,
            'user_id': session['user_id']
        }
        likes = like.Like.getAllLikes(info)
        print(likes)
        each.isLiked = like.Like.isLiked(info)
        print(each.isLiked)
        each.totalLikes = likes
    return render_template('onesReviews.html', currentUser=oneUser, animes=animes)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect('/')