#!/usr/bin/python3
#Written by redd-dedd of Parler Analysis Team

def print_readme():
    print('''
README
This script extracts images and videos from a specified warc file.
The files go into "./img" and "./vid",
relative to the current working directory.
The ./img and ./vid directories will be created if they do not already exist.
The exported filenames can be base64 decoded to reveal their target URIs.
The modified date/time is set to the value of Last-Modified HTTP header,
adjusted to local time.
(!) If you do not have a warc file:
    https://gist.github.com/Parler-Analysis/2c023fd2e053fba5bc85b09209f606eb
Example: python3 vidimg-extract.py filename.warc
''')

import base64
import os
import sys
import time
import email.utils as eut
from datetime import datetime

def validate_command():
    if len(sys.argv) < 2:
        print_readme()
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print_readme()
        print('\nERROR: %s file not found' % sys.argv[1])
        sys.exit(1)

def verify_output_dirs():
    if not os.path.isdir('img'):
        os.mkdir('img')
    if not os.path.isdir('vid'):
        os.mkdir('vid')

def extract():

    def get_extension(line):
        extension = 'unknown.bin'
        if b'jpeg' in line:
            extension = 'jpg'
        elif b'png' in line:
            extension = 'png'
        elif b'gif' in line:
            extension = 'gif'
        elif b'mp4' in line:
            extension = 'mp4'
        elif b'x-matroska' in line:
            extension = 'mkv'
        return extension

    def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    f = open(sys.argv[1], 'rb')

    while True:
        line = f.readline()
        if not line: break
        if b'WARC-Target-URI' in line:
            b64uri = base64.encodebytes(line.split(b' ')[1].strip()).decode().replace('\n', '')
        is_image = b'Content-Type: image' in line
        is_video = b'Content-Type: video' in line
        if is_image or is_video:
            extension = get_extension(line)
            if is_image:
                filename = 'img/%s.%s' % (b64uri, extension)
            elif is_video:
                filename = 'vid/%s.%s' % (b64uri, extension)
            nextline = f.readline()
            size = int(nextline.split(b' ')[1].replace(b'\r\n', b''))
            timestamp = 0
            while True:
                nextline = f.readline()
                if b'Last-Modified' in nextline:
                    last_modified_value = nextline.split(b': ')[1].decode().replace('\r\n', '')
                    dt = datetime_from_utc_to_local(datetime(*eut.parsedate(last_modified_value)[:6]))
                    timestamp = dt.timestamp()
                if nextline == b'\r\n':
                    contents = f.read(size)
                    img = open(filename, 'wb')
                    img.write(contents)
                    img.close()
                    os.utime(filename, (timestamp, timestamp))
                    print(filename)
                    break

if __name__ == '__main__':
    validate_command()
    verify_output_dirs()
    extract()
