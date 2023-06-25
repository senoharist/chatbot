from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

# table objecting
tabled = db['dmss']


## modul select db table dms
# modul select all dist
def fetch_dbd_alld():
    dmss = []
    for dms in tabled:
        dmss.append(dms)
    return dmss

# modul select dist by nomor wa
def fetch_dbd(wa_no):  # Each dms scnerio
    return tabled.find_one(wa_no=wa_no, order_by = '-id')

# modul to list depo
def fetch_depo():
     distinct_values = list(tabled.distinct('depo_code', 'depo_name'))
     return distinct_values

# modul to list dist by depo code
def fetch_dist(depo_code):
    distinct_values = list(tabled.distinct('dist_code', 'dist_name', depo_code=depo_code)) # , order_by ='-depo_code'))
    return distinct_values

# modul to show input data by depo_code
def fetch_dbdepo(depo_code):  # Each book scnerio
    return tabled.find_one(depo_code=depo_code) # , order_by = '-id')


## start to define route api
@app.route('/api/dbd_populate', methods=['GET'])
def dbd_populate():
    tabled.insert({
        "dist_code": "443501",
        "dist_name": "MUSS jombang",
        "depo_code": "3344",
        "depo_name": "depo surabaya",
        "dms_email": "akbar",
        "wa_no": "081122334455"
    })

    tabled.insert({
        "dist_code": "440101",
        "dist_name": "Affandison Gresik",
        "depo_code": "3243",
        "depo_name": "depo surabaya",
        "dms_email": "akbar",
        "wa_no": "085566778899"
    })

    return make_response(jsonify(fetch_dbd_alld()),
                         200)


# get and post dms data
@app.route('/api/dms', methods=['GET', 'POST'])
def api_dmss():
    if request.method == "GET":
        return make_response(jsonify(fetch_dbd_alld()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        tabled.insert(content)
        return make_response(jsonify(fetch_dbd(wa_no), 201))  # 201 = Created

# get data dms by wa no
@app.route('/api/dms/<wa_no>', methods=['GET', 'PUT', 'DELETE'])
def api_each_dms(wa_no):
    if request.method == "GET":
        dms_obj = fetch_dbd(wa_no)
        if dms_obj:
            return make_response(jsonify(dms_obj), 200)
        else:
            return make_response(jsonify(dms_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        tabled.update(content, ['wa-no'])
        dms_obj = fetch_dbd(wa_no)
        return make_response(jsonify(dms_obj), 200)
    elif request.method == "DELETE":
        tabled.delete(id=wa_no)
        return make_response(jsonify({}), 204)

# modul to list depo
@app.route('/api/depo', methods=['GET', 'POST'])
def api_depo():
    if request.method == "GET":
        return make_response(jsonify(fetch_depo()), 200)
    elif request.method == 'POST':
        content = request.json
        depo_code = content['depo_code']
        tabled.insert(content)
        return make_response(jsonify(fetch_dbdepo(depo_code), 201))  # 201 = Created

# modul to list dist by depo code
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
        tabled.update(content, ['dist_code'])
        dms_obj = fetch_dist(depo_code)
        return make_response(jsonify(dms_obj), 200)
    elif request.method == "DELETE":
        tabled.delete(id=depo_code)
        return make_response(jsonify({}), 204)


'''

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

'''
# table chat objecting
tablew = db['traffics']

## modul select db table chat
# fet list chat by wa no
def fetch_db(wa_no):  # Each chat scnerio
    return tablew.find_one(wa_no=wa_no, order_by = '-id')

# list of all chat
def fetch_db_all():
    traffics = []
    for wac in tablew:
        traffics.append(wac)
    return traffics

## route end-point

'''
@app.route('/api/db_populated', methods=['GET'])
def db_populated():
    tablew.insert({
        "dist_email": "443501@mailinator.com",
        "dist_name": "MUSS jombang",
        "question": "tampilan sahabat warung tidak seperti biasanya",
        "dist_code": "depo surabaya",
        "product": "B2B",
        "wa_no": "081122334455"
    })

    tablew.insert({
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
# list of all chat route
@app.route('/api/wac', methods=['GET', 'POST'])
def api_traffics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        tablew.insert(content)
        return make_response(jsonify(fetch_db(wa_no), 201))  # 201 = Created

# list of chat by wa no
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
