# from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import datetime
import requests
from flask import Flask, make_response, jsonify, request
import dataset


app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

# table = db['conversation WA']
tablew = db['traffics']


def fetch_db(wa_no):  # Each chat scnerio
    return tablew.find_one(wa_no=wa_no, order_by = '-id')


def fetch_db_all():
    traffics = []
    for wac in tablew:
        traffics.append(wac)
    return traffics

def send_email_notification(data):
    # Replace the following placeholders with your email server settings and email content
    create_date = data['updated_at'] + datetime.timedelta(hours=7)
    smtp_server = 'mail.pratesis.com'
    smtp_port = 587
    sender_email = 'scyllainsight@pratesis.com'
    sender_password = 'Pratesis123!'
    email_dist = data['dist_email']
    email_dist = email_dist.strip()
    receiver_email = 'agus_suryono@gmail.com' + "," + email_dist + "," + 'indra_s@pratesis.com'  # l1-support.central@pratesis.com
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


@app.route('/api/wac', methods=['GET', 'POST'])
def api_traffics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        wa_no = content['wa_no']
        tablew.insert(content)
     #  return make_response(jsonify(fetch_db(wa_no), 201))  # 201 = Created

     #  Call the webhook when new data is inserted
        webhook_url = 'http://127.0.0.1:5000/webhook'
        # webhook_data = {'wa_no': wa_no, 'product': product, 'question' : question}
        response = requests.post(webhook_url, json=content)
        # print("Webhook response:", response.text)
        return make_response(jsonify(fetch_db(wa_no), 201))  # 201 = Created

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data1 = request.json
    wa_no = data1['wa_no']
    data = fetch_db(wa_no)
    # Process the data received from the webhook

    # Insert your logic here to handle the new data
    # print("Received webhook data:", data)

    # Send email notification
    send_email_notification(data)
    return jsonify({'message': 'Webhook received successfully2'}), 200

if __name__ == '__main__':
    app.run(debug=True)
