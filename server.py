from flask import Flask, render_template, request
import json

app = Flask(__name__)

mp4_file_path = 'media/tomfriedman.mp4'

@app.route("/")
def index():
    return render_template('index.html', mp4_file_path=mp4_file_path)

@app.route("/get_video")
def get_video():
    print(request.headers)
    range_pos = request.headers['range']
    if not range_pos:
        return
    
    return render_template('index.html', mp4_file_path=mp4_file_path)
    

