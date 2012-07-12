def touch_wsgi_file():
    import os
    with file(os.environ['WSGI_FILE_PATH'], 'a'):
        os.utime(os.environ['WSGI_FILE_PATH'], None)
