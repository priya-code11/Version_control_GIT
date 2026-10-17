import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)
db = client.test
collection = db['User_info']


@app.route('/')
def home():
    return "Get data from /api endpoint to see the date and time. /get_data to retrieve all submitted data."

@app.route('/api/<name>/<int:age>/<dep>')
def show_data(name, age, dep):
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', date=date , name=name, age=age , dep=dep)

@app.route('/submit', methods=['POST'])
def submit_form():
    data=request.form.to_dict()
    try:
        collection.insert_one(data)
        return render_template('submit.html')
    except Exception as e:
        return render_template('index.html', error=str(e))
    
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/submittodoitem',methods=['GET','POST'])
def submit_todo():
    data=request.form.to_dict()
    try:
        collection.insert_one(data)
        return render_template('todo.html')
    except Exception as e:
        return render_template('todo.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)