import SpotifyGraph
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

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
        l = [(n.nodeVal, n.spotifyLink) for n in path]
        return render_template('link_path.html', data=l)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
