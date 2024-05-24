from flask import Flask, jsonify
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route('/mpesa_payment', methods=['POST'])
def mpesa_payment():
    # Prompt for inputs via terminal
    phone = input('Enter phone number (e.g., 0712345678): ')
    amount = input('Enter amount: ')

    # Ensure the phone number is in the international format
    if phone.startswith('0'):
        phone = '254' + phone[1:]

    # Generating the access token
    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"

    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    data = r.json()
    access_token = "Bearer " + data['access_token']

    # Getting the password
    timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    business_short_code = "174379"
    data_to_encode = business_short_code + passkey + timestamp
    encoded = base64.b64encode(data_to_encode.encode())
    password = encoded.decode('utf-8')

    # Body or payload
    payload = {
        "BusinessShortCode": "174379",
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
        "AccountReference": "account",
        "TransactionDesc": "account"
    }

    # Populating the HTTP header
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return jsonify({"success": "Paid {} - {}".format(phone, amount)}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
