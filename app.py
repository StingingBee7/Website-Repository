from flask import Flask, render_template, request, redirect
import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET = 'kylerfileupload' 

s3 = boto3.client('s3')

app = Flask(__name__)

@app.route('/')
def index():
	try:
		response = s3.list_objects_v2(Bucket=S3_BUCKET)
		files = [obj['Key'] for obj in response.get('Contents', [])]
	except NoCredentialsError:
		files = []

	signed_urls = []
	for file in files:
		url = s3.generate_presigned_url('get_object',
										Params={'Bucket': S3_BUCKET, 'Key': file},
										ExpiresIn=3600)
		signed_urls.append(url)

	return render_template('index.html', files=signed_urls)

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
        return redirect(f'/{file.filename}')

@app.route('/success')
def upload_success():
    return 'File successfully uploaded to S3!'

@app.route('/resume')
def resume():
    return render_template('ClayResume.html')

@app.route('/<filename>')
def get_file(filename):
    try:
        file_obj = s3.get_object(Bucket=S3_BUCKET, Key=filename)
        return file_obj['Body'].read()
    except s3.exceptions.NoSuchKey:
        return "File not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
