from flask import Flask, render_template, request
from flask_uploads import UploadSet, IMAGES, configure_uploads

import os

app = Flask(__name__)

#configure uploads
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
app.config["UPLOADS_DEFAULT_DEST"] = TOP_LEVEL_DIR + '/uploads/img/'
app.config["UPLOADED_IMAGES_DEST"] = TOP_LEVEL_DIR + '/uploads/img/'

images_upload_set = UploadSet('images', IMAGES)
configure_uploads(app, images_upload_set)
#end configure uploads

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    filename = images_upload_set.save(image)
    return filename

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)