import base64
from flask import jsonify
import requests

paypal = {
    # Live
    # "BASE_URL": "https://api-m.paypal.com",
    # "CLIENT_ID": "",
    # "APP_SECRET": "",

    # Sandbox
    "BASE_URL": "https://api-m.sandbox.paypal.com",
    "CLIENT_ID": "AfOliK5c_IXq5fN0TTqqeqEFF_NxbB5C6-gOD_vjtT1lhBvjvKXTe_igHxSS8kf3dOsQh57Un42AbA6R",
    "APP_SECRET": "EFo8QyW7WWPIpTwUySHWvHeMgOkKVdk2UA88uqL1SX-ad4BKW0tyO4ONK8MTw1z6O9PBGSm_yC_Fikq6",

    "CURRENCY": "USD",
    "TOTAL_PRICE": 107,
}

BASE_URL = paypal["BASE_URL"]
CLIENT_ID = paypal["CLIENT_ID"]
APP_SECRET = paypal["APP_SECRET"]
CURRENCY = paypal["CURRENCY"]
TOTAL_PRICE = paypal["TOTAL_PRICE"]


def create_order(invoice):
    data = gen_paypal_json(invoice)
    response = paypal_request("/v2/checkout/orders", json_data=data)
    data = response.json()
    return data, response.status_code


def capture_payment(order_id):
    url = BASE_URL + f"/v2/checkout/orders/{order_id}/capture"
    access_token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)

    data = response.json()
    return data, response.status_code


def gen_paypal_json(invoice):
    invoice = f"ORD_{invoice:0>10}"
    paypal_json = {"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": CURRENCY, "value": TOTAL_PRICE}, "invoice_id": invoice}]}
    return paypal_json


def generate_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    auth = base64.b64encode(f"{CLIENT_ID}:{APP_SECRET}".encode("utf-8")).decode("utf-8")


    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth}",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    json_data = response.json()
    access_token = json_data.get("access_token")

    return access_token


def paypal_request(url, json_data=None, request_method="POST"):
    url = BASE_URL + url
    access_token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    if json_data:
        headers["Content-Type"] = "application/json"
    
    if request_method == "GET":
        response = requests.get(url, headers=headers)
    elif json_data:
        response = requests.post(url, headers=headers, json=json_data)
    else:
        response = requests.post(url, headers=headers)
    return response


def paypal_order_detail(order_id):
    response = paypal_request(f'/v2/checkout/orders/{order_id}', request_method="GET")
    return response.json(), response.status_code
