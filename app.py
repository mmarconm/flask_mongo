from flask import Flask, redirect, url_for, request, render_template, flash
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Secret'

# client = MongoClient('192.168.0.103')
client = MongoClient("mongodb://mmarconm:admin@localhost/tododb") # defaults to port 27017

db = client.tododb


@app.route('/')
def todo():

    _items = db.tododb.find()
    count = db.tododb.find().count()
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
            db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    user = db.tododb.find({"id": id})

    if request.method == "POST":
        item_doc = {
            'email': request.form['email'],
            'name': request.form['name'],
            'language': request.form['language']
        }

        if item_doc['name'] and item_doc['language'] and item_doc['email']:
            db.tododb.update({"id": id}, {'$set': {"name": item_doc['name']}})
            db.tododb.update({"id": id}, {'$set': {"email": item_doc['email']}})
            db.tododb.update({"id": id}, {'$set': {"language": item_doc['language']}})
            flash('User {} Updated'.format(item_doc['name']))
            return redirect(url_for('todo'))

    return render_template('update.html', user=user)

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete(id):
    if id:
        item_doc = {
            "id": id
        }
        db.tododb.remove(item_doc)
        flash("User Deleted !")
        return redirect(url_for('todo'))

    return 'Wrong'

@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    if db.tododb.find().count() > 0:
        db.tododb.drop()
        flash('Removed All Users from Database')
        return redirect(url_for('todo'))

    flash('There is not users to delete in Database')
    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
