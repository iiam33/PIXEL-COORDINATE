import os
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import requests
from osgeo import gdal
import json

UPLOAD_FOLDER = 'static/img'
BASE = 'http://127.0.0.1:5000'

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_to_png(file_path):
   f_name = file_path.replace(UPLOAD_FOLDER, "")
   f_name = f_name.replace("\\", "")
   name = '.' in f_name and f_name.split('.')[0].lower()
   new_file_name = name + '.png'

   processed_img = Image.open(file_path)
   processed_img.thumbnail(processed_img.size)
   processed_img.save(f'{UPLOAD_FOLDER}/{new_file_name}', 'PNG', quality=100)
   return f"{UPLOAD_FOLDER}/{new_file_name}"

def convert_to_tiff(file_path):
   return

@app.route('/', methods=['GET','POST'])
def init():
   return render_template('index.html')
	
@app.route('/upload-file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      uploaded_file = request.files['file']
      file_name = secure_filename(uploaded_file.filename)
      uploaded_file.save(os.path.join(UPLOAD_FOLDER, file_name))
      processed_img = convert_to_png(os.path.join(UPLOAD_FOLDER, file_name))
      response = jsonify({'file': processed_img, 'message' : 'File successfully uploaded', 'status': 201})
      response.status_code = 201
      # return redirect(url_for('image', file = processed_img), response.status_code, response)
      # r = requests.post(BASE + '/image/' + processed_img)
      # return redirect(url_for('image', file = processed_img))
      return response

@app.route('/image', methods = ['GET'])
def image():
   res = requests.post(BASE + '/upload-file')
   # file = json.loads(res)
   file = res.json()
   # file = request.args.get('file-name')
   return render_template("image.html", image = file['file'])

# @app.route('/get-coordinate', methods = ['GET'])
# def get_coordinate():
#    name = "Block1994067ha_Orthomosaic_export_WedNov10094326109252"
#    f_name = name + ".tif"
#    file_path = os.path.join(UPLOAD_FOLDER, f_name)
#    response = jsonify({'file-name': name, 'pixels' : {'x': 1000, 'y': 2000}, 'status': 201})
#    return response
   
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)