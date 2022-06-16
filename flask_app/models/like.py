from flask_app.config.mysqlconnection import connectToMySQL
from .user import User
from flask import flash

class Like:
    db_name = "soloproject"
    
    def __init__(self, data):
        self.user_id = data['user_id']
        self.anime_id = data['anime_id']

    @classmethod
    def getAllLikes(cls, data):
        query = "SELECT * FROM likes where anime_id = %(anime_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likes = 0
        print(results)
        if not results :
            return likes
        for num in results:
            likes +=1
        return likes

    @classmethod 
    def save(cls, data):
        query = "insert into likes (user_id, anime_id) value ( %(user_id)s, %(anime_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results


    @classmethod
    def unlike(cls, data):
        query  = "DELETE FROM likes WHERE user_id = %(user_id)s and anime_id = %(anime_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def isLiked(cls, data):
        query = "SELECT * FROM likes LEFT JOIN users ON likes.user_id = users.id where anime_id = %(anime_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for likes in results:
            print(likes['user_id'])
            if data['user_id'] == likes['user_id']:
                return True
        return False

