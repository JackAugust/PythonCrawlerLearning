import os

dir = r"D:/Movie/"
dir2 = r"D:/Let'sFunning/Movie/"
string=os.listdir(dir)
for i in range(len(os.listdir(dir))):
	tmp=dir2+str(string[i])
	if not os.path.exists(tmp):
				os.makedirs(tmp)