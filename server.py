from flask import Flask, render_template, request, Response, send_file
import os

app = Flask(__name__)

CHUNK_SIZE = 10 ** 6

DEFAULT_VIDEO_NAME = 'eecs388lab5.mp4'

@app.route("/")
def index():
    return render_template('index.html')

def generate_data():
    for i in range(10):
        yield f"Data {i}\n"

@app.route('/video')
def video():
    video_path = 'static/media/eecs388lab5.mp4'
    print(video_path)
    return send_file(video_path, as_attachment=False)

@app.route('/get_video_full')
@app.route('/get_video_full/<video>')
def get_video_full(video=DEFAULT_VIDEO_NAME):
    video_path = f"static/media/{video}"
    print(video_path)

    range_header = request.headers.get('Range')
    if not range_header:
        return Response(status=200)  # If no range header, send the entire video

    total_size = os.path.getsize(video_path)
    start, end = get_range_from_header(range_header, total_size)
    content_length = end - start + 1

    with open(video_path, 'rb') as video_file:
        video_file.seek(start)
        data = video_file.read(content_length)
    response = Response(data, status=206)  # 206 Partial Content
    response.headers.add('Content-Range', f'bytes {start}-{end}/{total_size}')
    response.headers.add('Content-Length', content_length)
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Type', 'video/mp4')
    return response

@app.route('/get_video')
@app.route('/get_video/<video>')
def get_video(video=DEFAULT_VIDEO_NAME):
    video_path = f"static/media/{video}"
    range_header = request.headers.get('Range')
    if not range_header:
        return Response(status=200)  # If no range header, send the entire video

    total_size = os.path.getsize(video_path)
    start = int(range_header.replace('bytes=', '').split('-')[0])
    end = min(start + CHUNK_SIZE, total_size - 1)

    content_length = end - start + 1
    with open(video_path, 'rb') as video_file:
        video_file.seek(start)
        data = video_file.read(content_length)
    response = Response(data, status=206)  # 206 Partial Content
    response.headers.add('Content-Range', f'bytes {start}-{end}/{total_size}')
    response.headers.add('Content-Length', content_length)
    response.headers.add('Accept-Ranges', 'bytes')
    response.headers.add('Content-Type', 'video/mp4')
    return response

def get_range_from_header(range_header, total_size):
    parts = range_header.replace('bytes=', '').split('-')
    start = int(parts[0])
    end = min(int(parts[1]) if parts[1] else total_size - 1, total_size - 1)
    return start, end

if __name__ == '__main__':
    app.run()


