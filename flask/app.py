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


@app.route('/', methods=['GET'])
def index():
 
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    search_terms = request.args.get('search_terms')
    # sql = "SELECT * FROM Employee WHERE FirstName LIKE '%{}%'".format(search_terms)
    sql = "SELECT * FROM Employee WHERE FirstName LIKE %s"
    cursor.execute(sql, ['%' + search_terms + '%'])
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

"""
1. We need a route to show the form for adding a new one
2. We need a route to process the form for adding a new one
3. We need a route to show the form for editing the existing data
4. We need a route to process the form for editing the existing data
5. We need a route to show all the records for a table (Read in the CRUD)
6. We need a route to delete a record from a table
"""
@app.route('/mediatype')
def show_mediatype():
    # 1. we need a database cursor
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
   
    # 2. We need a SQL statement
    sql = "SELECT * FROM MediaType WHERE deleted=0"
    
    # 3. We have a cursor, we have a statement
    cursor.execute(sql)
    
    #4. We need to show the results
    # If there is only one result: we can use cursor.fetchone()
    results = []
    for r in cursor:
        results.append(r)
        
    #5. pass the results to a template
    return render_template('mediatype.html', data=results)
 

@app.route('/new/mediatype', methods=['GET'])
def new_mediatype():
    #1. show the form
    return render_template('new_mediatype.html', mediatype={})
    
@app.route('/new/mediatype', methods=['POST'])
def create_new_mediatype():
    #0. Create SQL cursor
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    
    #1. retrieve whatever data the user typed into the form
    media_type_name = request.form.get('media_type_name')
    
    #OPTIONAL 
    #If the database didn't use auto increment for the primary key, then
    #we have to calculate the next id ourselves
    
    sql = "SELECT MAX(MediaTypeId) AS'max_id' FROM MediaType";
    cursor.execute(sql)
    current_max_id = cursor.fetchone()['max_id']
    next_id = current_max_id + 1
    
    #2. Create the insert statement
    sql = "INSERT INTO MediaType (MediaTypeId, Name) VALUES (%s, %s)"
    
    #3. Excute the query
    cursor.execute(sql, [next_id, media_type_name])
    
    #4. Commit to the database to make the transaction permanent.
    connection.commit()
    
    #5. redirect to the listing page
    return redirect(url_for('show_mediatype'))
    
@app.route('/edit/mediatype/<mediaTypeID>')
def edit_media_type(mediaTypeID):
    #1 Retrieve the existing information for the media type we have selected
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM MediaType WHERE MediaTypeId = %s"
    cursor.execute(sql, [mediaTypeID])
    mediatype = cursor.fetchone()
    
    #1 Show the form

    
    return render_template('edit_mediatype.html', mediatype=mediatype)

@app.route('/delete/confirm/mediatype/<mediaTypeID>')
def confirm_delete_mediatype(mediaTypeID):
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM MediaType where MediaTypeId = %s"
    cursor.execute(sql, [mediaTypeID])
    mediatype = cursor.fetchone()
    
    return render_template('confirm_delete_mediatype.html', mediatype=mediatype)
    
@app.route('/delete/mediatype/<mediaTypeID>', methods=['POST'])
def delete_mediatype(mediaTypeID):
    cursor =  connection.cursor(pymysql.cursors.DictCursor)
    # sql = "DELETE FROM MediaType WHERE MediaTypeId = %s"
    sql = "UPDATE MediaType SET deleted = 1 WHERE MediaTypeId = %s"
    cursor.execute(sql, [mediaTypeID])
    connection.commit()
    return redirect(url_for('show_mediatype'))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)