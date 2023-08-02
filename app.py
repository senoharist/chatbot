import datetime

from flask import Flask, make_response, jsonify, request
import dataset
import smtplib
from email.mime.text import MIMEText
import requests

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

# modul to show one data by dist_code
def fetch_dist_one(dist_code):  # Each book scnerio
    return tabled.find_one(dist_code=dist_code) # , order_by = '-id')

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
            # a=print("data tidak ada")
            return make_response(jsonify(dms_obj), 404)

    elif request.method == "PUT":  # Updates the wa_no
        content = request.json
        dist_code = content.get('dist_code')
        new_wa_no = wa_no
        query = f"UPDATE dmss SET wa_no = '{new_wa_no}' WHERE dist_code = '{dist_code}'"
        db.query(query)
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

# modul to pick one dist by dist code
@app.route('/api/dist/<dist_code>', methods=['GET']) # , 'PUT', 'DELETE'])
def api_one_dist(dist_code):
    if request.method == "GET":
        dms_obj = fetch_dist_one(dist_code)
        if dms_obj:
            return make_response(jsonify(dms_obj), 200)
        else:
            return make_response(jsonify(dms_obj), 404)

    elif request.method == "PUT":  # Updates the book
        content = request.json
        tabled.update(content, ['dist_code'])
        dms_obj = fetch_dist(dist_code)
        return make_response(jsonify(dms_obj), 200)
    elif request.method == "DELETE":
        tabled.delete(id=dist_code)
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

# modul to send notif other case coming
def send_email_notification(data):
    # Replace the following placeholders with your email server settings and email content
    create_date = data['updated_at'] + datetime.timedelta(hours=7)
    smtp_server = 'mail.pratesis.com'
    smtp_port = 587
    sender_email = 'scyllainsight@pratesis.com'
    sender_password = 'Pratesis123!'
    email_dist = data['dist_email']
    email_dist = email_dist.strip()
    receiver_email = 'seno.harist@gmail.com' + "," + email_dist + "," + 'indra_s@pratesis.com'  # l1-support.central@pratesis.com
    cc_email = ['ruslan@pratesis.com','agus_suryono@pratesis.com']
    bcc_email = ['suseno.harist@gmail.com']
    subject = f"New case from {data['dist_name']}"
    body = f"Dear support, \n\n\nNew request coming and need responed from this below users : " \
           f"\n\nDistributor : {data['dist_name']}"\
           f"\nCode : {data['dist_code']}"\
           f"\nE-mail : {data['dist_email']}"\
           f"\nContact wa: {data['wa_no']}"\
           f"\nProduct : {data['product']}"\
           f"\nDetail case : {data['question']}" \
           f" \n\n\nWarm regards \n chatbot" \
           f"\nCreated at : {create_date}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # msg['Cc'] = cc_email
    # msg['Bcc'] = bcc_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email.split(","), msg.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print("Error sending email notification:", str(e))

# modul hooks to sending notify by email
@app.route('/kait', methods=['POST'])
def handle_kait():
    data1 = request.json
    wa_no = data1['wa_no']
    data = fetch_db(wa_no)
    # Process the data received from the webhook
    # Insert your logic here to handle the new data
    # print("Received webhook data:", data)

    # Send email notification
    send_email_notification(data)
    return jsonify({'message': 'notif received successfully'}), 200

## route end-point

# list of all chat route
@app.route('/api/wac', methods=['GET', 'POST'])
def api_traffics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        tablew.insert(content)
        #  Call the webhook when new data is inserted
        webhook_url = 'http://127.0.0.1:5000/kait'
        # webhook_data = {'wa_no': wa_no, 'product': product, 'question' : question}
        response = requests.post(webhook_url, json=content)
        # print("sending response:", response.text)
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
