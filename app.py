from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

DB_NAME = "pet_shop"

app = Flask(__name__)


def get_client():
    client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    return client

@app.route('/')
def index():
    client = get_client()
    animals = client[DB_NAME].animals.find()
    return render_template('index.template.html', animals=animals)


@app.route('/animal/create')
def create_animal():
    uploadcare_public_key = os.environ.get('UPLOADCARE_PUBLIC_KEY')
    return render_template('create_animal.template.html',
                           uploadcare_public_key=uploadcare_public_key)


@app.route('/animal/create', methods=["POST"])
def process_create_animal():
    client = get_client()
    client[DB_NAME].animals.insert_one({
        "name": request.form.get('animal_name'),
        "image": request.form.get("animal_image")
    })
    return "Data receieved"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
