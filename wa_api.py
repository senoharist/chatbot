from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

# table = db['books']
tablew = db['traffics']


def fetch_db(wa_no):  # Each chat scnerio
    return tablew.find_one(wa_no=wa_no, order_by = '-id')


def fetch_db_all():
    traffics = []
    for wac in tablew:
        traffics.append(wac)
    return traffics

'''
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
'''

@app.route('/api/wac', methods=['GET', 'POST'])
def api_traffics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        tablew.insert(content)
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
        tablew.update(content, ['wa_no'])

        wac_obj = fetch_db(wa_no)
        return make_response(jsonify(wac_obj), 200)
    elif request.method == "DELETE":
        tablew.delete(id=wa_no)

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)
