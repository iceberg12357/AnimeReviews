from flask_app.config.mysqlconnection import connectToMySQL
from .user import User
from flask import flash

class Anime:
    db_name = "soloproject"
    
    def __init__(self, data):
        self.user_id = data['user_id']
        self.id = data['id']
        self.title = data['title']
        self.creator = data['creator']
        self.year = data['year']
        self.platform = data['platform']
        self.thoughts = data['thoughts']
        self.genre = data['genre']
        self.firstName = data['firstName'] or ''
        self.totalLikes = 0
        self.isLiked = False

    @classmethod
    def getAllAnimes(cls):
        query = "SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id"
        results = connectToMySQL(cls.db_name).query_db(query)
        animes = []
        print(results)
        for anime in results:
            animes.append(cls(anime))
        return animes

    @classmethod
    def getAllAnimesByUser(cls, data):
        query = "SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id where animes.user_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        animes = []
        print(results)
        for anime in results:
            animes.append(cls(anime))
        return animes

    @classmethod
    def save(cls, data):
        query = "insert into animes (user_id, title, creator, year, platform, genre, thoughts) value (%(user_id)s, %(title)s, %(creator)s, %(year)s, %(platform)s, %(genre)s, %(thoughts)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def getAnime(cls, data):
        query = "SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id Where animes.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print("----------------", results)
        anime = cls(results[0])
        return anime

    @classmethod
    def update(cls, data):
        print (data)
        query = "UPDATE animes SET title = %(title)s, creator = %(creator)s, year = %(year)s, platform = %(platform)s, genre = %(genre)s, thoughts = %(thoughts)s WHERE id = %(id)s;"
        print(query)
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM animes WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def animeValidation(input):
        isValid = True
        if len(input['title']) < 3:
            flash("Please provide a title of at least 3 characters")
            isValid= False
        if len(input['creator']) < 3:
            flash("Please provide a creator name of at least 3 characters")
            isValid= False
        if input['year'] == 1900:
            flash("Please provide a year after 1900")
            isValid= False
        if len(input['platform']) < 1:
            flash("Please provide a platform to watch on")
            isValid= False
        if len(input['genre']) < 1:
            flash("Please seclect a genre")
            isValid= False
        if len(input['thoughts']) < 10:
            flash("Please provide your thoughts at least 10 characters")
            isValid= False

        return isValid


