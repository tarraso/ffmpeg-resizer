from flask import Flask, flash, request, redirect, url_for, send_from_directory
from celery import Celery
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
import ffmpeg

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']


# set up celery client
client = Celery(app.name, 
    broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)


@client.task(bind=True)
def convert(self, filename, scale='1280x720', codec='h264', bitrate="1500k", profile="high"):
    path = os.path.join(app.config['UPLOAD_FOLDER'],f"{self.request.id}.mp4")
    ffmpeg.input(filename)\
        .filter('scale', size=scale, force_original_aspect_ratio='increase')\
        .output(path, format=codec, **{'b:v': bitrate})\
        .run()


@app.route('/upload_file', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        scale = request.form.get("scale", "1280x720")
        codec = request.form.get("codec", "h264")
        bitrate = request.form.get("bitrate", "1500k")
        profile = request.form.get("profile", "")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            eager = convert.delay(path)
            return {
                "body":url_for("download", task_id=eager.id)
            }


@app.route('/download/<task_id>')
def download(task_id):
    state = client.AsyncResult(task_id).state
    if state == "SUCCESS":
        return send_from_directory(app.config['UPLOAD_FOLDER'], f"{task_id}.mp4", as_attachment=True)
    else:
        return {
            "state":state
        }

    
if __name__ == '__main__':
    app.run(debug=True)
