import SpotifyGraph
from flask import Flask, render_template

application = Flask(__name__)

g = SpotifyGraph.makeSpotifyGraph('OUTPUT_DATA.txt')

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/findlink')
def findLink():
    return render_template('find_link.html')

@application.route('/search')
def searchArtist():
    pass

if __name__ == "__main__":
    # uncomment the below line to run some sample query
    # print ([f.nodeVal for f in g.run('Sanjay Joseph', 'Shankar Mahadevan')])
    application.run(debug=True)
