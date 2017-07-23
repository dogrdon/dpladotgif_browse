# Flask
from flask import Flask, request, render_template

# Mongo
from pymongo import MongoClient
import bson.json_util


app = Flask(__name__)

client = MongoClient()
db = client.dplabrowser

RECORDS_PER_PAGE = 20

# Calculate offsets for fetching lists of flights from MongoDB
def get_navigation_offsets(offset1, offset2, increment):
	offsets = {}
	offsets['Next'] = {'top_offset': offset2 + increment, 'bottom_offset': 
	offset1 + increment}
	offsets['Previous'] = {'top_offset': max(offset2 - increment, 0), 
	'bottom_offset': max(offset1 - increment, 0)} # Don't go < 0
	return offsets


@app.route('/gifs')
def source():

	aws_base = "https://s3.amazonaws.com/dpladotgif/"

	start = request.args.get('start') or 0
	start = max(int(start) - 1, 0)
	end = request.args.get('end') or 20
	end = int(end)
	width = end - start

	nav_offsets = get_navigation_offsets(start, end, RECORDS_PER_PAGE)

	gifs = db.gifs.find().skip(start).limit(width)
	gif_count = gifs.count()

	return render_template('gifs.html', nav_path=request.path, nav_offsets=nav_offsets, gifs=gifs, gif_count=gif_count, aws_base=aws_base)

if __name__ == "__main__":
	app.run(debug=True)
