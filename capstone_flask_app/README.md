33.4.4: Capstone Step 11: Deployment Implementation

Need to update notes below from previous flask app:

1. Created a notebook file running on local jupyter server to verify code is working locally. This included creating the static and tempales folders with the style sheet and index.html files. Uploaded to GitHub at https://github.com/stjoha81/Capstone_2023_2024/blob/main/Flask.ipynb 

2. Created an app.py file that starts up ngrok and prompts for authtoken, then runs the index.html file on the local URL and renders a matplotlib graph based on inputs provided to the index.html page. Added my_flask_app_path to allow for adjusting path for different computers this code may run on.

3. Ran app.py via command line. ngrok works appropriately, and the local URL displays the index.html page and accepts inputs. Rendring of the graph fails due to a warning about rendering outside main thread. Specific error message:

UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
  fig, ax = plt.subplots(figsize=(12,8))
*** Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: 'NSWindow should only be instantiated on the main thread!'


