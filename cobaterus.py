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
    return tabled.find_one(wa_no=wa_no, order_by='-id')

# modul update wa by PUT methods used

def update_wa(wa_no):
    wa_update = tabled.update(wa_no = wa_no, where={'dist_code': 'dist_code1'})
    return wa_update

# modul to list depo
def fetch_depo():
    distinct_values = list(tabled.distinct('depo_code', 'depo_name'))
    return distinct_values


# modul to list dist by depo code
def fetch_dist(depo_code):
    distinct_values = list(tabled.distinct('dist_code', 'dist_name', depo_code=depo_code))  # , order_by ='-depo_code'))
    return distinct_values


# modul to show input data by depo_code
def fetch_dbdepo(depo_code):  # Each book scnerio
    return tabled.find_one(depo_code=depo_code)  # , order_by = '-id')


## start to define route api

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

    elif request.method == "PUT":  # Updates the record
        content = request.json
        dist_code = content.get('dist_code')
        new_wa_no = wa_no  # Use the value from the route as the new wa_no

        # Perform the update using the dist_code as the condition
        # tabled.update({'wa_no': new_wa_no}, ['dist_code = :dist_code1'], dist_code=dist_code)
        query = f"UPDATE dmss SET wa_no = '{new_wa_no}' WHERE dist_code = '{dist_code}'"
        db.query(query)

        # Fetch the updated record and return the response
        dms_obj = fetch_dbd(wa_no)
        return make_response(jsonify(dms_obj), 200)

    elif request.method == "DELETE":
        tabled.delete(wa_no="wa_no")
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
@app.route('/api/depo/<depo_code>', methods=['GET'])  # , 'PUT', 'DELETE'])
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
    return tablew.find_one(wa_no=wa_no, order_by='-id')


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
