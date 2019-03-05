import SpotifyGraph

g = SpotifyGraph.makeSpotifyGraph('OUTPUT_DATA.txt')


if __name__ == "__main__":
    print ([f.nodeVal for f in g.run('Sanjay Joseph', 'Shankar Mahadevan')])
