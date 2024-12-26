import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras_preprocessing import image 
from keras.models import load_model 
from keras.applications.vgg16 import preprocess_input
import numpy as np
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

#Create an app object using the Flask class. 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model=load_model('model.h5')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():     
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output
@app.route('/predict',methods=['POST'])
def predict():
    if 'fileUpload' not in request.files:
        return render_template('index.html', prediction_text='No file part')
    
    file = request.files['fileUpload']
    if file.filename == '':
        return render_template('index.html', prediction_text='No selected file')

    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    # Ensure the directory exists before saving the file
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
            file.save(file_path)

            img = image.load_img(file_path, target_size=(224, 224))
            imagee = image.img_to_array(img)  # Converting the X-Ray into pixels
            imagee = np.expand_dims(imagee, axis=0)
            img_data = preprocess_input(imagee)
            prediction = model.predict(img_data)
            
            if prediction[0][0] > prediction[0][1]:
                return render_template('services.html', prediction_text='Prediction: Person is safe')
            else:
                return render_template('services.html', prediction_text='Prediction: Person is affected by Pneumonia')

    else:
        return render_template('index.html', prediction_text='Invalid file format')



if __name__ == "__main__":
    app.run()