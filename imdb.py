from flask import Flask, render_template, request, redirect, url_for, session, json, send_file
import mysql.connector

# establish connection to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="newsletter"   # db name
)
# define cursor on the connection
cursor = connection.cursor()

# creating a flask instance
app = Flask(__name__)

# declare a secret key for sessions (encryption and decryption)
app.secret_key = 'this is a random secret key'


# login method
@app.route('/login', methods=['GET', 'POST'])
def login():
    # when POST request is made the check for the login credentials
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        # credentials verified
        if userid == 'admin' and password == '123':
            # save the userid in session
            session['userid'] = userid
            return render_template('editmovies.html')
        # when admin credentials not verified correctly
        else:
            return 'wrong credentials'
    # when GET request is made, return the login page
    return render_template('login.html')


# add movie method to add the movies when admin is logged in
@app.route('/addmovie', methods=['GET', 'POST'])
def addmovie():
    # if request == POST then, add the movie to the database
    if request.method == 'POST':
        # get various movie data from the http page
        popularity = request.form.get('99popularity')
        director = request.form.get('director')
        imdb_score = request.form.get('imdb_score')
        name = request.form.get('name')
        genre = request.form.get('genre')

        # execute query for inserting the data into the database
        cursor.execute("insert into movies(99popularity, director, imdb_score, name, genre) values(%s,%s,%s,%s,%s)", (popularity, director, imdb_score, name, ' '.join(genre.split())))
        # commit to reflect the changes to the database
        connection.commit()
        return 'movie data added to the database'
    # when admin is not logged in, return to the login page
    if 'userid' not in session:
        return redirect(url_for('login'))
    # when admin is logged in and GET request is made, return the editmovies page
    # editmovies.html have two options, one for adding moving and other for deleting movie
    return render_template('editmovies.html')


# deletemovie method to delete movie when admin is logged in
@app.route('/deletemovie', methods=['Get', 'POST'])
def deletemovie():
    # if request == POST then, delete the movie from the database
    if request.method == 'POST':
        # variable will contain (name, genre, director, imdb_score greater than, imdb_score less than)
        # to search a movie based on a particular criteria
        option = request.form.get('option')
        # this variable will contain the text entered by user that we need to search in the database
        value = request.form.get('value')
        adr = (value.lower(),)
        # delete movies that have 'value' (variable) as director name
        if option == 'director':
            sql = "delete from movies where lower(director) = %s"
            # execute the query
            cursor.execute(sql, adr)
            # commit to make changes reflect in the database
            connection.commit()
            return 'deleted successfully'
        # delete movies that have imdb_score greater than 'value' (variable)
        elif option == 'imdb_score_g':
            sql = "delete from movies where imdb_score >= %s"
            cursor.execute(sql, adr)
            connection.commit()
            return 'deleted successfully'
        # delete movies that have imdb_score less than 'value' (variable)
        elif option == 'imdb_score_l':
            sql = "delete from movies where imdb_score <= %s"
            cursor.execute(sql, adr)
            connection.commit()
            return 'deleted successfully'
        # delete movies that have 'value' (variable) as movie name
        elif option == 'name':
            sql = "delete from movies where lower(name) = %s"
            cursor.execute(sql, adr)
            connection.commit()
            return 'deleted successfully'
        # delete movies that have 'value' (variable) as genre
        elif option == 'genre':
            cursor.execute("delete from movies where lower(genre) like '%{}%'".format(value))
            connection.commit()
            return 'deleted successfully'
    # if admin is not logged in, return to login page
    if 'userid' not in session:
        return redirect(url_for('login'))
    # when admin is logged in and GET request is made, return the editmovies page
    # editmovies.html have two options, one for adding moving and other for deleting movie
    return render_template('editmovies.html')


# home page for all users
# users can search for a movie by name, genre, director, imdb_score greater than, imdb_score less than
@app.route('/home', methods=['GET', 'POST'])
def home():
    # when POST request is made, fetch the movie details from the database and give a json file containing output
    if request.method == 'POST':
        # variable will contain (name, genre, director, imdb_score greater than, imdb_score less than)
        # to search a movie based on a particular criteria
        option = request.form.get('option')
        # this variable will contain the text entered by user that we need to search in the database
        value = request.form.get('value')
        adr = (value.lower(),)
        # open file in write mode to write data in json format and return back to the user
        with open('output.json', 'w') as f:
            # fetch the movies that have 'value' (variable) as director name
            if option == 'director':
                sql = "select * from movies where lower(director) = %s"
                # execute the sql query
                cursor.execute(sql, adr)
                # loop over the cursor to get all movies one by one
                for item in cursor.fetchall():
                    # dictionary to store the movie details
                    data = {'name': item[1], '99popularity': item[2], 'director': item[3], 'imdb_score': item[4], 'genre': list(item[5].strip().split(' '))}
                    # convert the data to json format
                    j = json.dumps(data)
                    # write json data into the file
                    f.write(j + '\n')
            # fetch the movies that have imdb_score greater than 'value' (variable)
            elif option == 'imdb_score_g':
                sql = "select * from movies where imdb_score >= %s"
                cursor.execute(sql, adr)
                for item in cursor.fetchall():
                    data = {'name': item[1], '99popularity': item[2], 'director': item[3], 'imdb_score': item[4], 'genre': list(item[5].strip().split(' '))}
                    j = json.dumps(data)
                    f.write(j + '\n')
            # fetch the movies that have imdb_score less than 'value' (variable)
            elif option == 'imdb_score_l':
                sql = "select * from movies where imdb_score <= %s"
                cursor.execute(sql, adr)
                for item in cursor.fetchall():
                    data = {'name': item[1], '99popularity': item[2], 'director': item[3], 'imdb_score': item[4], 'genre': list(item[5].strip().split(' '))}
                    j = json.dumps(data)
                    f.write(j + '\n')
            # fetch the movies that have 'value' (variable) as movie name
            elif option == 'name':
                sql = "select * from movies where lower(name) = %s"
                cursor.execute(sql, adr)
                for item in cursor.fetchall():
                    data = {'name': item[1], '99popularity': item[2], 'director': item[3], 'imdb_score': item[4], 'genre': list(item[5].strip().split(' '))}
                    j = json.dumps(data)
                    f.write(j + '\n')
            # fetch the movies that have 'value' (variable) in its genre
            elif option == 'genre':
                cursor.execute("select * from movies where lower(genre) like '%{}%'".format(value))
                for item in cursor.fetchall():
                    data = {'name': item[1], '99popularity': item[2], 'director': item[3], 'imdb_score': item[4], 'genre': list(item[5].strip().split(' '))}
                    j = json.dumps(data)
                    f.write(j + '\n')
            # finally close the file
            f.close()
        # commit to make changes reflect in the database
        connection.commit()
        # return the json file containing result(movies searched)
        return send_file('output.json', attachment_filename='output.json')
    # when the GET request is made, return the home page
    return render_template('home.html')


# run the application
app.run(debug=True)
