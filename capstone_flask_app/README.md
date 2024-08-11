33.4.4: Capstone Step 11: Deployment Implementation


This capstone flask app was created based on previous iterations of the capstone project done in Jupyter notebook. The flask app provides a web UI for interacting wiht the capstoen machine learning model via APIs. The purpose of the app is for the user to upload an image of a MRI brain scan and for the model to predict whether the image contains one of 3 kinds of tumors, or no tumor at all. For production deployment, the flask app is packaged into a Docker image. The image can be run locally for test purposes, then uploaded to Docker Hub in preparation for production deployment. The production deployment uses the AWS Elastic Beanstalk service and leverages its associated monitoring and logging capabilities to keep track of the capstone application's health.

1. Build Docker image locally for test purposes: 
docker build -t capstone-flask-16 . 
The image can then be run locally with this command to test locally prior to cloud deployment: 
docker container run -d -p 5000:5000 capstone-flask-16

2. Build Docker image in preparation for production deployment: 
docker build --platform linux/amd64 -t stjoha8/capstonerep:latest3 .
There are a couple of important changes to this build command compared to the command in #1 above. First, it specifies the Docker Hub repository name. Second, since I was developing on a M3 Mac, the --platform option is needed to avoid warnings when deploying to a standard AWS Elastic Beanstalk managed service for running a docker container.

3. The command to push the image built in #2 to the Docker Hub is:
 docker push stjoha8/capstonerep:latest3 where stjoha8/capstonerep points to your Docker Hub repository.

4. The GitHub repository includes a Dockerrun.aws.json file. This is needed to actually get Elastic Beanstalk to pull the Docker Hub image over and deploy it. The Name field should be updated with your Docker Hub repository information. The Ports fields and logging fields can be updated if other ports or logging locations are preferred.

5. In AWS Elastic Beanstalk follow their step by step process for setting up a new environment, choosing Docker as the platform and then choose to upload a local file for the application. When you choose this, select the Dockerrun.aws.json referred to in step #4 above.

6. The time it takes to deploy the app in Elastic Beanstalk can vary. Around 20 minutes was typical. Once deployed, Elastic Beanstalk provides both a URL for calling the app (ex. http://capstoneapp8-env.eba-pv9rffx2.us-east-2.elasticbeanstalk.com/) and a robust set of metrics and ways of monitoring the application's health, including requests per second, number of responses, latency, and memory usage. The user can call the app and upload the JPEG formatted image of their choice. The app will then return the model's prediction of wther the image contains a meningiona, glioma, or pituitary tumor, or no tumor at all. 

7. Logging information can be downloaded from within the AWS console for Elastci Beanstalk. Navigate to the environment the app is running in, and select "Logs" on the left hand side. You can then choose whether to dwnload all of the log files or to download just the tail (last 100 lines) for each file to review.

8. Architecture diagram:
![Alt text](../Capstone_architecture_08112024.jpg?raw=true "Final Capstone architecture")








