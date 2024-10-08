from flask import Flask, render_template, request, redirect
import boto3
from botocore.exceptions import NoCredentialsError
import os

S3_BUCKET = 

s3 = boto3.client('s3')

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('index.html')

# hunter's contribution :)
a, b = 0, 1

@app.route("/fibonacci")
def fibonacci_iteration():
    global a, b
    current_fib = a
    a, b = b, a + b
    return f"<h1>Current Fibonacci Number: {current_fib}</h1>"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']
    if file.filename == '':
        return 'No file selected for upload'

    if file:
        #Fill in later using S3 code
        s3.upload_fileobj(file, S3_BUCKET, file.filename, ExtraArgs={'ContentType':file.content_type})
        return redirect('/success')

@app.route('/success')
def upload_success():
    return 'File successfully uploaded to S3!'
