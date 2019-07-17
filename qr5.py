#QR
# a qr encodeing engine for large files
#Designed By Duncan Andrews

#Libraries
try:

	import subprocess

	import os

	import os.path

	import fnmatch

	import qrcode

	import qrtools

	import binascii

	import cv2

	import numpy as np

	from os.path import isfile, join
except:
	print("you seem to be missing some libraries")

#GLOBAL VARIBLES



#Pause Function
def Pause():
	pase = raw_input("Press Enter.. ")
	return

def Banner():
#Prints banner and clear screen at each new page
	#clear screen
	os.system('cls' if os.name == 'nt' else 'clear')
	print("QR")
	print("__________________________________")
	#return to function that called
	return



def Hex():
	Banner()
	print("----------Working Directory Files ")
	#list files in working directory
	print("Files: ")
	listOfFiles = os.listdir('.')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			print(entry)
	#Read  file into HEX
	filename = raw_input("Enter file name: ")
	#remove file extension
	filenameraw = filename[:-4]
	with open(filename, 'rb') as f:
    		content = f.read()
	print(binascii.hexlify(content))
	HEXcontent=(binascii.hexlify(content))

	#Make new file into HEX
	try:
		file = open("HEX" + filenameraw + ".txt" ,"w")
		file.write(HEXcontent)
		file.close
		print("File HEX" + filename +"  made Succesfully!")
	except:
		print("File could not be made")
	Pause()
	return

def QRmake():
	Banner()
	print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
        listOfFiles = os.listdir('.')
        pattern = "*.txt"
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)

#Prompt for file name and directtory name
	filename= raw_input("Enter File Name: ")
	directoryName= raw_input("Enter Directory name to create: ")
#make a directory to put the image files into
	os.mkdir(directoryName)
#open file and measure length
	filenamefull = filename
	f = open(filenamefull, "r")
	fileContents = f.read()
	fileChar = len(fileContents)
	print("Character lengh of " + filenamefull + ": ")
	print(fileChar)
	Pause()
	f.close()
#loop through the file actualy creating the  qr codes


	name = 0
	nameCount= 0
	counter =  0
	#there are 2 hex vaules equals one byte
	while counter < fileChar:
		#if counter <= 0:
                #	counter = 0
		qr = qrcode.QRCode(
    			version=40,
    			error_correction=qrcode.constants.ERROR_CORRECT_M,
    			box_size=10,
    			border=4,
		)
	#make  the  amount of data to be encoded
		a = counter + 2000
		if a > fileChar:
			a = fileChar
                load = a / fileChar
		load = load * 100
                print("Percent Done: " + str(load))
		print("Characters Processed: " + str(a) + " of " + str(fileChar))
		a = a * -1

		payload = fileContents[counter:-a]
		print("Payload: ")
                print(payload)
		qr.add_data(payload)
		qr.make(fit=True)


		realname= str(nameCount) + ".png"
		location = directoryName + "/" + realname
		img = qr.make_image(fill_color="black", back_color="white")
		img.save(location)


	#adjust variables
		counter += 2000
		name += 1
		nameCount +=1

#finish the last bit of data if its less than  1200
#		if fileChar =0:
#			 a = fileChar * -1
#	                print(a)
#       	        payload = fileContents[counter:-a]
#                	qr.add_data(payload)
#                	print(payload)
#	               	qr.make(fit=True)


#               	realname= str(name) #+ ".jpg"
#                	img = qr.make_image(fill_color="black", back_color="white")
#                	img.save(realname)

		print(name)

	print("Finished")
	Pause()
	return
def QRread():
	Banner()
	print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
        listOfFiles = os.listdir('.')
        pattern = "*.png"
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)
	filename= raw_input("Enter QR file name: ")
	qr = qrtools.QR()
	qr.decode(filename)
	print qr.data
	Pause()
	return


def QRassemble():
	Banner()

	#make new file todump data
	f= open("HEXassemble.txt", "a")
	listOfFiles = os.listdir('.')
        pattern = "*.png"
	count = 1
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
			print(entry)
			count +=1


	#make cache to prevent duplicates qr
	cache= ""
	duplicate = 0
        i = 1
	while i < count:
        	qr = qrtools.QR()
		print(i)
		file = "image" + str(i)
        	qr.decode(file + ".png")
		#check cache
		if cache != qr.data:
			f.write(qr.data)
			print(file)
			print(qr.data)
		else:
			print("Duplicate Found")
			duplicate += 1
		i += 1
		cache = qr.data
	print(str(duplicate) + " Duplicates found.")
	f.close()
        Pause()
        return

def MMcreate():
	Banner()
	path = raw_input("Enter Folder of QR images to compile: ")
	path = "./" + path + "/"
	pathIn= path
	pathOut = 'video.avi'
	fps = 2.0
	frame_array = []
	files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
	#for sorting the file names properly
	files.sort(key = lambda x: x[5:-4])
	files.sort()
	frame_array = []
	files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
	#for sorting the file names properly
	files.sort(key = lambda x: int(filter(str.isdigit, x)))
	for i in range(len(files)):
	        filename=pathIn + files[i]
	        #reading each files
		print(filename)
	        img = cv2.imread(filename)
	        height, width, layers = img.shape
	        size = (width,height)

    #inserting the frames into an image array
	        frame_array.append(img)
	        out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
	Pause()
	for i in range(len(frame_array)):
	    # writing to a image array
	    out.write(frame_array[i])
	out.release()
	print("video.avi made!")
	Pause()
	return

def MMbreak():
	Banner()
	#liost files
	listOfFiles = os.listdir('.')
        pattern = "*.avi"
        count = 0
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)
                        count +=1
	file = raw_input("Enter File name: ")
	vidcap = cv2.VideoCapture(file)
	def getFrame(sec):
	    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
	    hasFrames,image = vidcap.read()
	    if hasFrames:
	        cv2.imwrite("image"+str(count)+".png", image)     # save frame as JPG file
	    return hasFrames
	sec = 0
	frameRate = 0.5 #//it will capture image in each 0.5 second
	count=1
	success = getFrame(sec)
	while success:
	    count = count + 1
	    sec = sec + frameRate
	    sec = round(sec, 2)
	    success = getFrame(sec)

	print("Video Deconstructed!")
	Pause()
	return

########################################################3
#Home Menu
def Home():
	#List Options
	Banner()
	print("1. Open File in Hex")
        print("2. MAke qr")
	print("3. Read QR")
	print("4. Reassemble bank")
	print("5. Create video")
	print("6. Deconstruct video")
        print("7. Quit")
        choice = raw_input("ENter CHoice: ")
        if choice:
                if choice == '1':
                        Hex()
                if choice == '2':
                        QRmake()
		if choice == '3':
                        QRread()

                if choice == '4':
                        QRassemble()
		if choice == '5':
                        MMcreate()
                if choice == '6':
                        MMbreak()
                if choice == '7':
			Banner()
                        quit()
	else:
		Home()
	Home()

Home()

