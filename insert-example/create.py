import pymysql

connection = pymysql.connect(host='localhost',
    user="admin",
    password="password",
    database="Chinook"
)

cursor = connection.cursor()

cursor.execute("SELECT MAX(ArtistId) FROM Artist")
next_id = cursor.fetchone()[0] + 1

artist_name = input("Please enter the name of the artist")
track = input("Please enter the name of the track")

sql = "INSERT INTO Artist (ArtistId, `Name`) VALUES (%s, %s)"
cursor.execute(sql, [next_id, artist_name])

new_artist_id = next_id

cursor.execute("SELECT MAX(AlbumId) FROM Album")
next_id = cursor.fetchone()[0] + 1

sql = "INSERT INTO Album (AlbumId, ArtistId, Title) VALUES ( %s, %s, %s)"
cursor.execute(sql, [next_id, new_artist_id, track])



# without commiting, won't be saved
connection.commit()

connection.close()