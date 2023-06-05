from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)  # create an instance of the Flask class called app

@app.route('/', methods=['GET', 'POST'])
def index():
    # if the request method is POST, then the user has submitted the form
    if request.method == 'POST':
        # we can access the data the user submitted by using the request object
        artist_name = request.form['artist']
        albums = search_albums(artist_name, 'name_asc')
        #sort_order = request.form.get('sort_order', 'name_asc')
        if albums is None:
            #return 'Artist not found'
            return render_template('results.html', artist=artist_name, albums=None)
        else:
            save_albums_to_db(artist_name, albums)
            return render_template('results2.html', artist=artist_name, albums=albums)
        #return render_template('index.html')
        #save_albums_to_db(artist_name, albums)
        #return render_template('results.html', artist=artist_name, albums=albums)
    return render_template('index.html')

'''
@app.route('/sort', methods=['POST'])
def sort():
    artist_name = request.form['artist']
    sort_order = request.form.get('sort_order', 'name_asc')
    albums = search_albums(artist_name, sort_order)
    return render_template('results.html', artist=artist_name, albums=albums)
'''

@app.route('/sort', methods=['GET'])
def sort():
    artist_name = request.args.get('artist')
    sort_order = request.args.get('sort_order', 'name_asc')
    print(sort_order)
    albums = search_albums(artist_name, sort_order)
    return render_template('results2.html', artist=artist_name, albums=albums)

def search_albums(artist_name, sort_order):
    API_KEY = '523532'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    response = requests.get(URL)
    data = response.json()
    #albums = data['album'] #
    #return albums
    albums = data.get('album')  # get will return None if 'album' key is not in data
    if albums:
        if sort_order == 'name_asc':
            albums.sort(key=lambda album: album['strAlbum'])
        elif sort_order == 'name_desc':
            albums.sort(key=lambda album: album['strAlbum'], reverse=True)
        elif sort_order == 'year_asc':
            albums.sort(key=lambda album: int(album['intYearReleased']))
        elif sort_order == 'year_desc':
            albums.sort(key=lambda album: int(album['intYearReleased']), reverse=True)
    return albums if albums else None  # return None if albums is an empty list

def save_albums_to_db(artist_name, albums):
    conn = sqlite3.connect('albums.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums
                 (artist TEXT, album TEXT, year INTEGER)''')

    for album in albums:
        artist = artist_name
        album_name = album['strAlbum']
        year = album['intYearReleased']

        # Check if the album is already in the database
        c.execute('''SELECT * FROM albums WHERE artist = ? AND album = ? AND year = ?''',
                  (artist, album_name, year))
        print(c.fetchone())
        # If the album is not in the database, insert it
        if not c.fetchone():
            c.execute("INSERT INTO albums VALUES (?,?,?)", (artist, album_name, year))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # run the app
