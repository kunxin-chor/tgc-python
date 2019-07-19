from flask import Flask, render_template, request
import os
import pymysql

connection = pymysql.connect(
    host='localhost', # IP address of the database; localhost means "the local machine"
    user="admin",  #the mysql user
    password="password", #the password for the user
    database="Chinook" #the name of database we want to use
)

app = Flask(__name__)


@app.route('/')
def index():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    # store results in a list
    results = []
    for r in cursor:
        results.append(r)
   
    return render_template('index.html', 
    data=results)

@app.route('/artist')
def artists():
     cursor = connection.cursor(pymysql.cursors.DictCursor)
     sql = "SELECT * FROM Artist"
     cursor.execute(sql)
     results = []
     for r in cursor:
         results.append(r)
     print(results)
     return render_template('artist.html', data=results)
     
@app.route('/album/<artistId>')
def albums(artistId):
     cursor = connection.cursor(pymysql.cursors.DictCursor)
     
     sql = "SELECT * FROM Artist Where ArtistId = {}".format(artistId)
     cursor.execute(sql)
     artist = cursor.fetchone()
     
     sql = "SELECT * FROM Album WHERE ArtistId = {}".format(artistId)
     cursor.execute(sql)
     results = []
     for r in cursor:
         results.append(r)
     print(results)
     return render_template('album.html', data=results, artist=artist)


@app.route('/music/track/<albumId>')
def track(albumId):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Track WHERE AlbumId = {}".format(albumId)
    print (sql)
    # cursor is NOT the results; cursor points to the result
    cursor.execute(sql)
    
    results = []
    for r in cursor:
        results.append(r)
        
    return render_template('track.html', data=results)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)