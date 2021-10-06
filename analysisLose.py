import numpy as np


year = "2021"
month = "February"


blackList = open("blackList.txt","r").read()
print("So lenh lo theo ngay:")
array = [0] * 32
lines = open("lose1.txt","r").readlines()
for line in lines:
	line=line.replace("\n","")
	line = line.split("  ")
	if len(line)==2:
		line = line[1]

		line = line.split(" start =")[0].replace("date = ","").replace(" 00","")
		# line = line.split(" ")
		if year in line:
			if month in line:
				line = line.split(" ")[0]

				array[int(line)]=array[int(line)]+1
				# print(str(line)+"  "+ str(array[int(line)]))
for i in range(0,len(array)-1):
	print(str(i+1)+": "+str(array[i+1]))

print("So lenh lai theo ngay:")
array = [0] * 32
lines = open("win1.txt","r").readlines()
for line in lines:
	line=line.replace("\n","")
	line = line.split("  ")
	if len(line)==2:
		line = line[1]

		line = line.split(" start =")[0].replace("date = ","").replace(" 00","")
		# line = line.split(" ")
		if year in line:
			if month in line:
				line = line.split(" ")[0]

				array[int(line)]=array[int(line)]+1
				# print(str(line)+"  "+ str(array[int(line)]))
for i in range(0,len(array)-1):
	print(str(i+1)+": "+str(array[i+1]))

a1=0
a2=0
a3=0
a4=0
a5=0
a6=0
a7=0
a8=0
a9=0
a10=0
a11=0
a12=0
lines = open("lose1.txt","r").readlines()
for line in lines:
	line=line.replace("\n","")
	line = line.split("  ")
	if len(line)==2:
		line = line[1]

		line = line.split(" start =")[0].replace("date = ","").replace(" 00","")
		# line = line.split(" ")
		if year in line:
			if "January" in line:
				a1+=1
			if "February" in line:
				a2+=1
			if "March" in line:
				a3+=1
			if "April" in line:
				a4+=1
			if "May" in line:
				a5+=1
			if "June" in line:
				a6+=1
			if "July" in line:
				a7+=1
			if "August" in line:
				a8+=1
			if "September" in line:
				a9+=1
			if "October" in line:
				a10+=1
			if "November" in line:
				a11+=1
			if "December" in line:
				a12+=1
print("So lenh lo theo thang")
print("a1="+str(a1))
print("a2="+str(a2))
print("a3="+str(a3))
print("a4="+str(a4))
print("a5="+str(a5))
print("a6="+str(a6))
print("a7="+str(a7))
print("a8="+str(a8))
print("a9="+str(a9))
print("a10="+str(a10))
print("a11="+str(a11))
print("a12="+str(a12))


a1=0
a2=0
a3=0
a4=0
a5=0
a6=0
a7=0
a8=0
a9=0
a10=0
a11=0
a12=0
lines = open("win1.txt","r").readlines()
for line in lines:
	line=line.replace("\n","")
	line = line.split("  ")
	if len(line)==2:
		line = line[1]

		line = line.split(" start =")[0].replace("date = ","").replace(" 00","")
		# line = line.split(" ")
		if year in line:
			if "January" in line:
				a1+=1
			if "February" in line:
				a2+=1
			if "March" in line:
				a3+=1
			if "April" in line:
				a4+=1
			if "May" in line:
				a5+=1
			if "June" in line:
				a6+=1
			if "July" in line:
				a7+=1
			if "August" in line:
				a8+=1
			if "September" in line:
				a9+=1
			if "October" in line:
				a10+=1
			if "November" in line:
				a11+=1
			if "December" in line:
				a12+=1
print("So lenh lai theo thang")
print("a1="+str(a1))
print("a2="+str(a2))
print("a3="+str(a3))
print("a4="+str(a4))
print("a5="+str(a5))
print("a6="+str(a6))
print("a7="+str(a7))
print("a8="+str(a8))
print("a9="+str(a9))
print("a10="+str(a10))
print("a11="+str(a11))
print("a12="+str(a12))





# ### tinh blackList

# pair = ["a"]*1000
# meWin = [1000]*1000
# meLose = [0]*1000
# count=0
# winLines = open("win1.txt","r").readlines()
# for line in winLines:
# 	line=line.replace("\n","")
# 	if len(line)>10:
# 		line = line.split(" ")
# 		word="123"
# 		for a in line:
# 			if "USDT" in a:
# 				word=a
# 		if word != "123":
# 			found=0
# 			for i in range(0,count+1):	
# 				if word == pair[i]:
# 					meWin[i]+=1
# 					found=1
# 					break

# 			if found==0:
# 				count+=1
# 				pair[count]=word
# 				meWin[count]=1

# loseLines = open("lose1.txt","r").readlines()
# for line in loseLines:
# 	line=line.replace("\n","")
# 	if len(line)>10:
# 		line = line.split(" ")
# 		word="123"
# 		for a in line:
# 			if "USDT" in a:
# 				word=a
# 		if word != "123":
# 			found=0
# 			for i in range(0,count+1):	
# 				if word == pair[i]:
# 					meWin[i]-=1
# 					meLose[i]-=1
# 					found=1
# 					break


# for i in range(0,count):
# 	if meWin[i]>4:
# 		print(pair[i]+"  "+str(meWin[i])+"  "+str(meLose[i]))
# 	else:
# 		open("blackList.txt1","a").write(pair[i]+"\n")
# 	# if meWin[i] - meLose[i,""]>5:
# 	# 	print(pair[i]+"  "+str(meWin[i])+"  "+str(meLose[i]))