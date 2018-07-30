from flask import Flask, redirect, url_for, request, render_template, flash
from pymongo import MongoClient
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'Secret'

client = MongoClient('192.168.0.103')
db = client.tododb


@app.route('/')
def todo():

    _items = db.tododb.find()
    count = db.tododb.find().count()
    items = [item for item in _items]

    return render_template('todo.html', items=items, count=count)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'id': uuid4().hex,
        'name': request.form['name'],
        'description': request.form['description']
    }

    if item_doc['name'] and item_doc['description']:
        db.tododb.insert_one(item_doc)
    else:
        return redirect(url_for('todo'))

    flash('User Saved !')
    return redirect(url_for('todo'))

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
