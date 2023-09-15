# Importing the required modules
from flask import Flask, request, jsonify, render_template

# Importing the datetime module for timestamp
from datetime import datetime

# Creating a Flask app object
app = Flask(__name__)

# Defining the route for the index page
@app.route("/test", methods=["GET", "POST"])
def test():
    print("hello human")
    return jsonify({"inference": "positive!!"})

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    print("heeeey")
    app.run(debug=True)