from flask import Flask, make_response, jsonify, request
from dataset import connect
import dataset


app = Flask(__name__)
db = connect('sqlite:///api.db')

'''
Examples:
GET request to /api/books returns the details of all books
POST request to /api/books creates a book with the ID 3 (As per request body)

Sample request body -
{
        "book_id": "1",
        "name": "A Game of Thrones",
        "author": "George R. R. Martin"
}

GET request to /api/books/3 returns the details of book 3
PUT request to /api/books/3 to update fields of book 3
DELETE request to /api/books/3 deletes book 3

'''

# table = db['books']
table = db['dmss']


def fetch_db(wa_no):  # Each book scnerio
    return table.find_one(wa_no=wa_no, order_by = '-id')

def fetch_db_all():
    dmss = []
    for dms in table:
        dmss.append(dms)
    return dmss

'''
@app.route('/api/db_populate', methods=['GET'])
def db_populate():
    table.insert({
        "dist_code": "443501",
        "dist_name": "MUSS jombang",
        "depo_code": "3344",
        "depo_name": "depo surabaya",
        "dms_email": "akbar",
        "wa_no": "081122334455"
    })

    table.insert({
        "dist_code": "440101",
        "dist_name": "Affandison Gresik",
        "depo_code": "3243",
        "depo_name": "depo surabaya",
        "dms_email": "akbar",
        "wa_no": "085566778899"
    })

    return make_response(jsonify(fetch_db_all()),
                         200)
'''

@app.route('/api/dms', methods=['GET', 'POST'])
def api_dmss():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        dist_code = content['dist_code']
        table.insert(content)
        return make_response(jsonify(fetch_db(dist_code), 201))  # 201 = Created

def fetch_depo():
     distinct_values = list(table.distinct('depo_code', 'depo_name'))
     return distinct_values


def fetch_dist(depo_code):
    distinct_values = list(table.distinct('dist_code', 'dist_name', depo_code=depo_code)) # , order_by ='-depo_code'))
    return distinct_values


def fetch_dbdepo(depo_code):  # Each book scnerio
    return table.find_one(depo_code=depo_code) # , order_by = '-id')


@app.route('/api/depo', methods=['GET', 'POST'])
def api_depo():
    if request.method == "GET":
        return make_response(jsonify(fetch_depo()), 200)
    elif request.method == 'POST':
        content = request.json
        depo_code = content['depo_code']
        table.insert(content)
        return make_response(jsonify(fetch_dbdepo(depo_code), 201))  # 201 = Created

@app.route('/api/depo/<depo_code>', methods=['GET']) # , 'PUT', 'DELETE'])
def api_each_dist(depo_code):
    if request.method == "GET":
        dms_obj = fetch_dist(depo_code)
        if dms_obj:
            return make_response(jsonify(dms_obj), 200)
        else:
            return make_response(jsonify(dms_obj), 404)

    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['dist_code'])

        dms_obj = fetch_db(depo_code)
        return make_response(jsonify(dms_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=depo_code)

        return make_response(jsonify({}), 204)


@app.route('/api/dms/<dist_code>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(dist_code):
    if request.method == "GET":
        dms_obj = fetch_db(dist_code)
        if dms_obj:
            return make_response(jsonify(dms_obj), 200)
        else:
            return make_response(jsonify(dms_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['dist_code'])

        dms_obj = fetch_db(dist_code)
        return make_response(jsonify(dms_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=dist_code)

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)
