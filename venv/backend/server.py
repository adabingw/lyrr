from flask import Flask, request 
from flask_cors import CORS, cross_origin
from data import collect, get_artist
from model import generator

app = Flask(__name__)
CORS(app, support_credentials=True)

models = ['Lorde', 'Taylor Swift'] 

@app.route('/lyrics', methods=['POST'])
@cross_origin()
def get_lyrics(): 
    """ Get starting lyrics to generate from 
        args:
            lyrics: str
            artist: str
    """
    print("get lyrics") 
    lyrics = request.args.get('lyrics')
    artist = request.args.get('artist') 
    
    print(lyrics)
    print(artist)
    
    generated_lyrics = generator(text=lyrics, name=artist)
    return {
        'lyrics': generated_lyrics
    } 
    
@app.route('/new_model', methods=['POST'])
@cross_origin()
def generate_new_model(): 
    print("generate new model") 
    
@app.route('/artist', methods=['GET']) 
@cross_origin() 
def get_artists():
    """ Get artist information from artist name
        args:
            artist_name: str
    """
    print("get artist") 
    artists = get_artist(request.args.get('artist_name'))
    print(artists)
    return {
        'artist': artists
    }
    
if __name__ == "__main__":
    app.run(debug = True)
