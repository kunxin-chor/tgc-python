from flask import Flask, render_template, request, redirect, url_for
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
    
@app.route('/edit/employee/<employeeId>')
def edit_employee(employeeId):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Employee WHERE EmployeeId = {}".format(employeeId)
    cursor.execute(sql)
    employee = cursor.fetchone()
    
    return render_template('edit_employee.html', e=employee)
    
@app.route('/edit/employee/<employeeId>', methods=['POST'])
def update_employee(employeeId):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    title = request.form.get('title')
    sql = "UPDATE Employee SET FirstName = '{}', LastName='{}', Title='{}' WHERE EmployeeId = {}".format(
        first_name, last_name, title, employeeId
    )
    cursor.execute(sql)
    connection.commit()
    return redirect(url_for('index'))
    

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

@app.route('/new/artist/', methods=['GET'])    
def new_artist():
    return render_template('new_artist.html')
    
@app.route('/new/artist/', methods=['POST'])
def create_new_artist():
    artist_name = request.form.get('artist_name')
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT MAX(ArtistId) FROM Artist")
    next_id = cursor.fetchone()['MAX(ArtistId)'] 
    next_id = next_id + 1

    
    sql = "INSERT INTO Artist (ArtistId, Name) VALUES ({}, '{}')".format(next_id, artist_name)
    cursor.execute(sql)

    connection.commit()
    
    return "Artist has been created!"


@app.route('/edit/artist/<artistId>')
def edit_artist(artistId):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Artist WHERE ArtistId = {}".format(artistId))
    artist = cursor.fetchone()
    return render_template('edit_artist.html', artist=artist)

@app.route('/edit/artist/<artistId>', methods=['POST'])
def update_artist(artistId):
    
    artist_name = request.form.get('artist_name')
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("UPDATE Artist SET Name = '{}' WHERE ArtistId = {}".format(artist_name, artistId))
    
    connection.commit()
    return redirect(url_for('artists'))

@app.route('/new/album/')    
@app.route('/new/album/<artistId>')
def new_album(artistId=0):
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Artist"
    cursor.execute(sql)
    artists = []
    for r in cursor:
        artists.append({
            'ArtistId' : r['ArtistId'],
            'Name' : r['Name']
        })
    
    return render_template('new_album.html', data=artists,artist_id = int(artistId))
    
@app.route('/new/album', methods=['POST'])
def create_new_album():
    
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT MAX(AlbumId) FROM Album")
    next_id = cursor.fetchone()['MAX(AlbumId)']
    next_id += 1
    
    album_name = request.form.get('album_name')
    # artist variable will hold the artist id
    artist = request.form.get('artist')
    
    sql = "INSERT INTO Album (AlbumId, Title, ArtistId) VALUES({}, '{}', {})".format(next_id, album_name, artist)
    
    cursor.execute(sql)   

    connection.commit()
    return "Album created successfully!"

"""
Alternatively:
@app.route('/new/artist/', methods=['GET', 'POST'])    
def new_artist():
    if (request.method == "GET"):
     return render_template('new_artist.html')
    else:
     return "form submitted"
"""

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)