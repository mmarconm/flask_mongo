from flask import Flask, redirect, url_for, request, render_template, flash
# from pymongo import MongoClient, ASCENDING, DESCENDING
from flask_pymongo import PyMongo, pymongo
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Secret'
app.config['MONGO_URI'] = "mongodb://mmarconm:admin@localhost/tododb" # defaults to port 27017

mongo = PyMongo(app)

# client = MongoClient('192.168.0.103')
# client = MongoClient("mongodb://mmarconm:admin@localhost/tododb") # defaults to port 27017
# db = client.tododb

@app.route('/')
def todo():

    _items = mongo.db.tododb.find().sort('date', -1)
    count = mongo.db.tododb.find().count()
    items = [item for item in _items]

    return render_template('todo.html', items=items, count=count)


@app.route('/new', methods=['POST'])
def new():
    if request.method == "POST":
        item_doc = {
            'id': uuid4().hex,
            'date': datetime.now().strftime('%b %d %Y %I:%M%p'),
            'email': request.form['email'],
            'name': request.form['name'],
            'status': request.form['option'],
            'language': request.form['language']
        }

        if item_doc['name'] and item_doc['language'] and item_doc['email']:
            flash('User Saved !')
            mongo.db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    user = mongo.db.tododb.find({"id": id})

    if request.method == "POST":
        item_doc = {
            'email': request.form['email'],
            'name': request.form['name'],
            'language': request.form['language']
        }

        if item_doc['name'] and item_doc['language'] and item_doc['email']:
            for key in item_doc.keys():
                mongo.db.tododb.update({"id": id}, {'$set': {key: item_doc[key]}})
            flash('User {} Updated !'.format(item_doc['name']))
            return redirect(url_for('todo'))

    return render_template('update.html', user=user)

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete(id):
    if id:
        item_doc = {
            "id": id
        }
        mongo.db.tododb.remove(item_doc)
        flash("User Deleted !")
        return redirect(url_for('todo'))

    return 'Wrong'

@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    if mongo.db.tododb.find().count() > 0:
        mongo.db.tododb.drop()
        flash('Removed All Users from Database')
        return redirect(url_for('todo'))

    flash('There is not users to delete in Database')
    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
