# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

from ds_messenger import DirectMessenger

SERVER = "168.235.86.101"

senderName = "Cheese"
senderPass = "cake"
reciever = "spiderman"
message = "my weapon is better than ur spidysense"

if __name__ == "__main__":
	#connect user to server
	dMessenger = DirectMessenger(SERVER, senderName, senderPass)

	#send message to reciever
	dMessenger.send(message, reciever)

	#retirieve chats from server
	temp = dMessenger.retrieve_new()
	print("Retrieve new:", type(temp))
	print(temp)
	print("")

	
	temp = dMessenger.retrieve_all()
	print("Retrieve all:", type(temp))
	print(temp)