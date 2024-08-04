#import getpass
#from pyngrok import ngrok, conf

#print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/auth")
#conf.get_default().auth_token = getpass.getpass()

from datetime import datetime
from flask import Flask, render_template, request
import cv2
import threading
import io
import joblib
import numpy as np
import os
import base64

os.environ["FLASK_DEBUG"] = "development"

template_dir= "./templates"

app = Flask(__name__, template_folder=template_dir)
port = 5000

# Open a ngrok tunnel to the HTTP server
#public_url = ngrok.connect(port).public_url
#print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
#app.config["BASE_URL"] = public_url

# Load the finetuned model that was previously save out via joblib.
capstone_model = joblib.load("./models/capstone_model.joblib")
if (capstone_model):
    print("Model loaded...")
else:
    print("No model loaded!")

# Create a dictionary for mapping the prediction value to a tumor name.
tumor_name_dict = {"0":"glioma_tumor", "1":"meningioma_tumor", "2":"no tumor", "3":"pituitary_tumor" }


@app.route('/', methods=['GET', 'POST'])
def index():
    #chart_url = None

    # Set default value for prediction.
    prediction_value = ""

    if request.method == 'POST':
        # Extract an uploaded image from the request form and 
        # save it out for potential future retraining purposes.
        try:

            # Get the uploaded image file.
            uploaded_file = request.files["image_file"]

            # Save the uploaded image with a unique name based on 
            # combining the filename and timestamp.
            datetime_string = datetime.now().strftime("%Y%m%d-%H%M%S")
            #print("Saved filename", datetime_string+uploaded_file.filename)
            saved_filename = "./static/uploaded_images/" + datetime_string + "_" + uploaded_file.filename
            uploaded_file.save(saved_filename)
            

        except Exception as e:
            print("Image save error:")
            print(e)
            #return f"Error: {e}"

        # Need to prep the uploaded image before making a prediction.
        # Resize the image to 256 x 256 since that is the size iamges the model was trained on.
        image = cv2.imread(saved_filename)
        image_size = 256
        resized_image = cv2.resize(image,(image_size, image_size))

        # Add the resized image to an array.
        image_array = []
        image_array.append(resized_image)

        # Convert the image data into a numpy array so the model can understand it.
        np_image_array = np.array(image_array)
        
        # Use the loaded and finetuned capstone model to make a prediction.
        prediction = capstone_model.predict(np_image_array)
        print("Prediction:")
        print(prediction[0])
        array_index = 0
        while (array_index <= len(prediction[0])):
            if (prediction[0][array_index] == 1):
                # Look up tumor name based on predicted value.
                prediction_value = tumor_name_dict.get(str(array_index))
                #print("Predicted tumor type:", prediction_value)
                break                
            array_index += 1


        

    # Return a render_template function, passing the predicted value as input.
    return render_template("index.html", prediction_value=prediction_value)


#if __name__ == '__main__':
    # Start the Flask server in a new thread
#  threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()

if __name__ == '__main__':
    # Start the Flask server in a new thread
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000, "use_reloader": False}).start()
