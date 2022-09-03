# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

import ds_protocol
import socket
import json
import sys

username = 'kirito'
password = 'pass123'
port = 3021
server = '168.235.86.101'
message = "New Hello Test2"
recipient = 'Cheese'


def send(server: str, port: int, username: str, password: str, message: str, recipient: str):
    """
    Testing the join, send, and receive functions from ds protocol
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((server, port))
        except:
            print("Please enter a valid IP address. The system will now exit.")
            sys.exit()
        # test for joining server
        join_func = ds_protocol.join(username, password, '')
        client.sendall(join_func.encode('utf-8'))
        srv_msg = client.recv(4096).decode('utf-8')
        token, response = ds_protocol.extract_json(srv_msg)
        print("1:", response)

        # test for sending direct message
        sending_msg = ds_protocol.send_message(token, message, recipient)  # recipient
        client.sendall(sending_msg.encode('utf-8'))
        srv_msg = client.recv(4096).decode('utf-8')
        print("2:", json.loads(srv_msg)["response"]["message"])

        # test for receiving unread message
        rec_msg = ds_protocol.rec_message(token)
        client.sendall(rec_msg.encode('utf-8'))
        srv_msg = client.recv(4096).decode('utf-8')
        print("3:", srv_msg)

        # test for receiving all messages
        all_msg = ds_protocol.rec_all(token)
        client.sendall(all_msg.encode('utf-8'))
        srv_msg = client.recv(4096).decode('utf-8')
        print("4:", json.loads(srv_msg)["response"]["messages"])


send(server, port, username, password, message, recipient)
