import pickle
with open("ClassifyResults","r") as f:
    lines = f.readlines()
    id = 0
    users = []
    for line in lines:
    	if id == 21:
    		break
    	if id != 0:
	    	user = [u.lstrip().rstrip() for u in line.split("|") if u != '']
	    	users.append(user)
    	id += 1
save_file = open("20famous.pickle","wb")
pickle.dump(users,save_file)
save_file.close()