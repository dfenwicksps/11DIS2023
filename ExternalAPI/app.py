from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():  # This is the function that will be called when the user visits the index page.
    # If the user submits the form on the index page, then the request method will be POST.
    if request.method == 'POST':
        # We can access the data the user submitted by using the request object.
        artist_name = request.form['artist']
        # We can then pass this data to the search_albums function.
        albums = search_albums(artist_name)
        # We can then pass the artist name and albums to the results.html template.
        return render_template('results.html', artist=artist_name, albums=albums)
    # If the user visits the index page without submitting the form,
    # then the request method will be GET.
    return render_template('index.html')

def search_albums(artist_name):
    API_KEY = '523532'
    #URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/search.php?s={artist_name}'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    response = requests.get(URL)
    print(type(response))
    print(response)
    data = response.json()
    print(type(data))
    print(data)
    albums = data['album']
    return albums

if __name__ == '__main__':
    app.run(debug=True)