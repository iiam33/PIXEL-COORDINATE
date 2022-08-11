import os
from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'static/img'

app = Flask(__name__)
api = Api(app)

def convert_to_png(file_path):
   f_name = file_path.replace(UPLOAD_FOLDER, "")
   f_name = f_name.replace("\\", "")
   name = '.' in f_name and f_name.split('.')[0].lower()
   new_file_name = name + '.png'
 
   processed_img = Image.open(file_path)
   processed_img.thumbnail(processed_img.size)
   processed_img.save(f'{UPLOAD_FOLDER}/{new_file_name}', 'PNG', quality=100)
   return f"{UPLOAD_FOLDER}/{new_file_name}"

# def upload_file():
#    if request.method == 'POST':
#       uploaded_file = request.files['file']
#       file_name = secure_filename(uploaded_file.filename)
#       uploaded_file.save(os.path.join(UPLOAD_FOLDER, file_name))
#       processed_img = convert_to_png(os.path.join(UPLOAD_FOLDER, file_name))
#       response = jsonify({'file': processed_img, 'message' : 'File successfully uploaded', 'status': 201})
#       response.status_code = 201
#       return response

class File(Resource): 
    def get(self):
        return {"msg": "Got"}

    def post(self):
        uploaded_file = request.files['file']
        file_name = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, file_name))
        processed_img = convert_to_png(os.path.join(UPLOAD_FOLDER, file_name))
        response = jsonify({'file': processed_img, 'message' : 'File successfully uploaded', 'status': 201})
        response.status_code = 201
        return response

api.add_resource(File, "/upload-file")

@app.route('/', methods=['GET','POST'])
def init():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)