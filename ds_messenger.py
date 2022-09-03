# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

import socket
import time
import json
import ds_protocol

PORT = 3021

class DirectMessage(dict):
    """
    Stores the recipient message and time
    """
    def __init__(self, recipient = None, message = None, timestamp = None):
        self._recipient = recipient
        self._message = message
        self._timestamp = timestamp

        self.set_recipient(recipient)
        self.set_message(message)
        self.set_time(timestamp)

        dict.__init__(self, recipient=self._recipient, message=self._message, timestamp=self._timestamp)
        
    def set_recipient(self, recipient:str):
        self._recipient = recipient 
        dict.__setitem__(self, 'recipient', recipient)

    def get_recipient(self):
        return self._recipient

    def set_message(self, message:str):
        self._message = message
        dict.__setitem__(self, 'message', message)
    
    def get_message(self):
        return self._message

    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    def __str__(self):
        return f"Recipient: %s | Message: %s | Timestamp: %s" % (self.recipient, self.message, str(self.timestamp))

    recipient = property(get_recipient, set_recipient)
    message = property(get_message, set_message)
    timestamp = property(get_time, set_time)

# Send a directmessage to another DS user
#{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

# Request unread message from the DS server
#{"token":"user_token", "directmessage": "new"}

# Request all messages from the DS server
#{"token":"user_token", "directmessage": "all"}

class DirectMessenger:
    """
    Class that contains methods to send and receive data from the server
    """
    global PORT

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.is_connected = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                #join the server
                if not dsuserver == None and not username == None and not password == None:
                    #connect to server
                    client.connect((dsuserver, PORT))

                    send = client.makefile('w')
                    recv = client.makefile('r')
                    send_msg = '{"join": {"username": "%s", "password": "%s", "token": "%s"}}' % (username, password, '')
                    send.write(send_msg + '\r\n')
                    send.flush()
                    #receive message
                    srv_msg = recv.readline()
                    #get token
                    self.token = json.loads(srv_msg)["response"]["token"]
                    self.is_connected = True
        except:
            print("Can not connect to server")
            self.is_connected = False

    def send(self, message:str, recipient:str) -> bool:
        """
        returns true if message successfully sent, false if send failed.
        """
        global PORT
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, PORT))
                send = client.makefile('w')
                recv = client.makefile('r')

                sending_msg = ds_protocol.send_message(self.token, message, recipient)
                client.sendall(sending_msg.encode('utf-8'))

                response = ""
                srv_msg = recv.readline()
                try:
                    response = json.loads(srv_msg)["response"]["type"]
                except:
                    print("Could not send message. Please try again later.")

                if response == "ok":
                    return True
        except:
            print('Can not send while disconnected from the internet')
            return False

    def retrieve_new(self) -> list:
        """
        returns a list of DirectMessage objects containing all new messages
        """
        global PORT

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, PORT))
            send = client.makefile('w')
            recv = client.makefile('r')

            rec_msg = ds_protocol.rec_message(self.token)
            client.sendall(rec_msg.encode('utf-8'))
            srv_msg = recv.readline()
            return json.loads(srv_msg)["response"]["messages"]

    def retrieve_all(self) -> list:
        """
        returns a list of DirectMessage objects containing all messages
        """
        global PORT

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, PORT))
            send = client.makefile('w')
            recv = client.makefile('r')

            all_msg = ds_protocol.rec_all(self.token)
            client.sendall(all_msg.encode('utf-8'))
            srv_msg = recv.readline()
            return json.loads(srv_msg)["response"]["messages"]
