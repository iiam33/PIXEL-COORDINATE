import os
from urllib import response
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import requests

UPLOAD_FOLDER = 'assets'
BASE = 'http://127.0.0.1:5000'

app = Flask(__name__, template_folder="template")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_file(file_name):
   image_path = "assets"
   name = '.' in file_name and file_name.split('.')[0].lower()
   new_file_name = name + ".png"

   processed_img = Image.open(file_name)
   processed_img.thumbnail(processed_img.size)
   processed_img.save(f"{image_path}/{new_file_name}", "PNG", quality=100)
   return f"{image_path}/{new_file_name}"

# def get_file(file_name):
#    # return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)
#     file = open(file_name, 'rb').read()
#     response = requests.post(BASE + '/upload-file', data=file)
#     return response.json()


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
      # file_path = get_file(processed_img)
      # response = file_path
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