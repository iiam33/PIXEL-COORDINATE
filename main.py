import os
from urllib import response
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import requests

UPLOAD_FOLDER = 'static/img'
BASE = 'http://127.0.0.1:5000'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_file(file_name):
   name = '.' in file_name and file_name.split('.')[0].lower()
   new_file_name = name + ".png"

   processed_img = Image.open(file_name)
   processed_img.thumbnail(processed_img.size)
   processed_img.save(f"{UPLOAD_FOLDER}/{new_file_name}", "PNG", quality=100)
   return f"{UPLOAD_FOLDER}/{new_file_name}"

@app.route('/', methods=['GET','POST'])
def init():
   return render_template('index.html')
	
@app.route('/upload-file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      uploaded_file = request.files['file']
      file_name = secure_filename(uploaded_file.filename)
      uploaded_file.save(secure_filename(uploaded_file.filename))
      # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
      processed_img = convert_file(file_name)
      response = jsonify({'file-path': processed_img, 'message' : 'File successfully uploaded', 'status': 201})
      response.status_code = 201
      return redirect(url_for('image', file = processed_img))
   return response

@app.route('/image', methods = ['GET'])
def image():
   file = request.args.get('file')
   return render_template("image.html", image = file)
   
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)