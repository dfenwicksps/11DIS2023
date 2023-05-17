# SETUP routes


def search():
#BEGIN Search
    #INPUT Artist AS artist_name OR artist_name = INPUT Artist
    artist_name = request.form['artist']
    #VAR url = https://theaudiodb.com/api/v1/json/523532/searchalbum.php?s=artist_name
    URL = f'https://theaudiodb.com/api/v1/json/523532/searchalbum.php?s={artist_name}'
    #VAR response = GET artist_data from url
    response = requests.get(URL)
    #VAR data = format response
    #print(type(response))
    #print(response)
    data = response.json()
    #print(type(data))
    #print(data)
    #DISPLAY data AS results.html
    return render_template('results.html', artist=artist_name, albums=albums)
#END Search