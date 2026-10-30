from flask import Flask

# Create the web app
app = Flask(__name__)

# When someone visits the home page ("/"), run this function
@app.route("/")
def home():
    return "<h1>My Fridge</h1><p>Nothing tracked yet! We're getting somewhere though!</p>"

# Start the app when you run this file
if __name__ == "__main__":
    app.run(debug=True, port=5001)