import os
from datetime import datetime
import certifi
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

# Standard, secure connection via certifi
client = MongoClient(DATABASE_URL, tlsCAFile=certifi.where())
db = client.test
collection = db['User_info']
todo_collection = db['todos']


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

@app.route('/submittodoitem', methods=['GET', 'POST'])
def submit_todo():
    message = None
    error = None

    if request.method == 'POST':
        data = request.form.to_dict()
        # Only insert if form fields are not empty
        if data.get('itemName') or data.get('itemDescription'):
            try:
                todo_collection.insert_one(data)
                message = "Item added successfully!"
            except Exception as e:
                error = str(e)

    # Fetch all items to render in todo_2.html
    try:
        items = list(todo_collection.find())
        for item in items:
            item['_id'] = str(item['_id'])
    except Exception as e:
        items = []
        error = str(e)

    return render_template('todo.html', items=items, message=message, error=error)

if __name__ == '__main__':
    app.run(debug=True)