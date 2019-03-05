import SpotifyGraph, json
from flask import Flask, render_template, request, redirect, url_for

application = Flask(__name__)

g = SpotifyGraph.makeSpotifyGraph('OUTPUT_DATA.txt')

artists = [n.nodeVal for n in g.nodesList.values() if n.nodeType == 'Artist']

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/findlink')
def findLink():
    return render_template('find_link.html', artists=artists)

@application.route('/show', methods=['POST'])
def show():
    firstArtist = request.form.get('firstArtist')
    secondArtist = request.form.get('secondArtist')
    if firstArtist not in artists or secondArtist not in artists:
        redirect(url_for('findlink'))
    else:
        path = g.run(firstArtist, secondArtist)
        l = [n.nodeVal for n in path]
        return json.dumps(l)

if __name__ == "__main__":
    application.run(debug=True)
