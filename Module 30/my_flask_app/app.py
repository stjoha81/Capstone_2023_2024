import getpass
from pyngrok import ngrok, conf

print("Enter your authtoken, which can be copied from https://dashboard.ngrok.com/auth")
conf.get_default().auth_token = getpass.getpass()

from flask import Flask, render_template, request
import threading
import matplotlib.pyplot as plt
import io
import os
import base64

os.environ["FLASK_DEBUG"] = "development"

my_flask_app_path = "/Users/sh/Documents/School/UCSD Extension /Machine Learning and AI/Capstone/Project Files/Module 30/my_flask_app"
template_dir= my_flask_app_path + "/templates"

app = Flask(__name__, template_folder=template_dir)
port = 5000

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url


# 1.
# Added a parameter for item number 6 above to include a name supplied by the user.
def generate_bar_chart(categories, values, user_name):
    # Write code here for a fuction that takes a list of category names and
    # respective values and generates a bar chart using plt.bar. Return your
    # barplot as a UTF-8 encoded string.

    # Get the x values from the category names list.
    x = [category for category in categories]
    # Get the y values from the values list.
    y = [value for value in values]

    # Set the subplot.
    fig, ax = plt.subplots(figsize=(12,8))
    # Set the bar chart and labels.
    ax.bar(x,y)
    ax.set_title(user_name + "'s Category and Values chart")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")

    # Create IO buffer object.
    buffer = io.BytesIO()
    #Save the bar chart to the buffer.
    fig.savefig(buffer, format="png")

    # Return your barplot as a UTF-8 encoded string
    return base64.b64encode(buffer.getvalue()).decode()


@app.route('/', methods=['GET', 'POST'])
def index():
    chart_url = None

    if request.method == 'POST':
        # Extract categories from the request form and convert the string to a
        # list.

# 2.
        # Get the categories from the HTTTP request.
        categories_string = request.form["categories"]
        # Convert to list.
        categories = categories_string.split(",")

        # Extract values from the request form and convert the input string to a
        # list of integers.

        # Get the values from the HTTTP request.
        values_string = request.form["values"]

        # Convert to list of integers.
        values = [int(x) for x in values_string.split(",")]

# 6. See if you can extend it in some way.
# Make sure you understand how the python code interacts with the html template.

        # Get the user's name from the additional text box included in the html.
        user_name = request.form["your_name"]


# 3.
        # Pass your categories and values to the generate_bar_chart function.
        # also pass the additional name value included for item nubmer 6 above.
        chart_url = generate_bar_chart(categories, values, user_name)
# 4.
    # Return a render_template function, passing your bar plot as input.
    return render_template("index.html", chart_url=chart_url)


if __name__ == '__main__':
    # Start the Flask server in a new thread
  threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()