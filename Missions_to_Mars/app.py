from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mission_to_mars

app = Flask(__name__) 

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def call_to_scrape():
    mars = mongo.db.mars
    mars_data = scrape_mission_to_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__=="__main__":
    app.run(debug=True)
