from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

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
table = db['traffics']


def fetch_db(wa_no):  # Each book scnerio
    return table.find_one(wa_no=wa_no)


def fetch_db_all():
    traffics = []
    for wac in table:
        traffics.append(wac)
    return traffics


@app.route('/api/db_populated', methods=['GET'])
def db_populated():
    table.insert({
        "dist_email": "443501@mailinator.com",
        "dist_name": "MUSS jombang",
        "question": "tampilan sahabat warung tidak seperti biasanya",
        "dist_code": "depo surabaya",
        "product": "B2B",
        "wa_no": "081122334455"
    })

    table.insert({
        "dist_email": "440101@mailinator.com",
        "dist_name": "Affandison Gresik",
        "question": "kenapa saya tidak bisa login pagi ini ",
        "dist_code": "depo surabaya",
        "product": "OSDP",
        "wa_no": "085566778899"
    })

    return make_response(jsonify(fetch_db_all()),
                         200)


@app.route('/api/wac', methods=['GET', 'POST'])
def api_traffics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        table.insert(content)
        return make_response(jsonify(fetch_db(wa_no), 201))  # 201 = Created


@app.route('/api/wac/<wa_no>', methods=['GET', 'PUT', 'DELETE'])
def api_each_wa(wa_no):
    if request.method == "GET":
        wac_obj = fetch_db(wa_no)
        if wac_obj:
            return make_response(jsonify(wac_obj), 200)
        else:
            return make_response(jsonify(wac_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['wa_no'])

        wac_obj = fetch_db(wa_no)
        return make_response(jsonify(wac_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=wa_no)

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)
