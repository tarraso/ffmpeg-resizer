
1. Install requirements
```
$ pip install -r requirements
```
Install ffmpeg
```
$ sudo apt install ffmpeg
```

2. Start the Flask app
```
$ python app.py
```

3. Start celery 
```
$ clery -A app.client worker
```

Endpoints
POST: /upload_file
file - file for resize
