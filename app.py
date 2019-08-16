import os
import scrape_mars
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_final = scrape_mars.scrape_news()
    mars_final = scrape_mars.scrape_facts_table()
    mars_final = scrape_mars.scrape_image()
    mars_final = scrape_mars.scrape_weather()
    mars_final = scrape_mars.scrape_hemisphere()
    
    mars_data.update({}, mars_final, upsert=True)
    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
