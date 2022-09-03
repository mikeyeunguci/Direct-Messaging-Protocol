# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

import json
import time


def extract_json(json_msg: str):
    """
    Call the json.loads function to change the json_msg from a str to a dict and extracts the token & message using key value pairing
    """
    try:
        json_obj = json.loads(json_msg)
        token = json_obj["response"]["token"]
        response = json_obj["response"]["message"]
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    except KeyError:
        print("Please retry again with the correct username and password")
    return token, response


def join(username: str, password: str, my_public_key):
    """
    This function will organize the username and password in json format
    """
    join_str = {"join": {"username": username, "password": password, "token": my_public_key}}
    json_join_str = json.dumps(join_str)
    return json_join_str


def send_message(token: str, message: str, recipient: str):
    """
    This function sends a direct message to a user
    """
    send_str = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": time.time()}}
    json_send_str = json.dumps(send_str)
    return json_send_str


def rec_message(token: str):
    """
    This function receives unread messages from a user
    """
    rec_str = {"token": token, "directmessage": "new"}
    json_rec_str = json.dumps(rec_str)
    return json_rec_str


def rec_all(token: str):
    """
    This function receives all the messages from a user
    """
    rec_str = {"token": token, "directmessage": "all"}
    json_rec_str = json.dumps(rec_str)
    return json_rec_str
