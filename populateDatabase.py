import json
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="newsletter"
)

json_data = open('imdb.json').read()
json_obj = json.loads(json_data)
cursor = connection.cursor()



for item in json_obj:
    popularity = item.get('99popularity')
    director = item.get('director')
    imdb_score = item.get('imdb_score')
    name = item.get('name')
    genre = item.get('genre')
    genre = ' '.join(genre)
    cursor.execute("insert into movies(99popularity, director, imdb_score, name, genre) values(%s,%s,%s,%s,%s)", (popularity, director, imdb_score, name, ' '.join(genre.split())))
connection.commit()
connection.close()
