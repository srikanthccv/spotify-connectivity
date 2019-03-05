import SpotifyGraph
from flask import Flask, render_template

application = Flask(__name__)

g = SpotifyGraph.makeSpotifyGraph('OUTPUT_DATA.txt')

artists = [n.nodeVal for n in g.nodesList.values() if n.nodeType == 'Artist']

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/findlink')
def findLink():
    return render_template('find_link.html', artists=artists)


if __name__ == "__main__":
    application.run(debug=True)
