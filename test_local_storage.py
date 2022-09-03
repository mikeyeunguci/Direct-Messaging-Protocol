# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

from Profile import Profile
from ds_messenger import DirectMessenger

SERVER = "168.235.86.101"

senderName = "testtesttest6969"
senderPass = "pass"

if __name__ == "__main__":
	test_save = True

	#test saving
	if test_save:
		profile = Profile("168.235.86.101", "Cheese", "cake")

		dMessenger = DirectMessenger(SERVER, senderName, senderPass)

		profile.dms = dMessenger.retrieve_all()

		profile.save_profile("./test.dsu")

	#test loading
	else:
		profile = Profile()
		profile.load_profile("./test.dsu")

		print(profile.username)
		print(profile.password)

