
#QR
# a qr encodeing engine for large files
#Designed By Duncan Andrews

#Libraries
try:

	import time

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

	from moviepy.editor import VideoFileClip, concatenate_videoclips

	from decimal import Decimal as D

	from pathlib import Path

        from zipfile import ZipFile


except:
	print("you seem to be missing some libraries")

#GLOBAL VARIBLES
#these are used for the steps function

#50 is the default amount of images to process at once into a video clip
x = 10
b = 0
path = 0


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
  
  
#compress whatever file(s) you want to
def Zip():
        Banner()
        print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
        listOfFiles = os.listdir('.')
        pattern = "*"
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)
                
                
        fileName = raw_input("Enter file to compress: ")
        zf = ZipFile('my_python_files.zip','w')
        zf.write(fileName)
        Pause()
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
	if filename == "":
                return
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
	if filename == "":
                return
	directoryName= raw_input("Enter Directory name to create: ")
	if directoryName == "":
                return
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
		a = counter + 1500
		if a > fileChar:
			a = fileChar
	#calculate the percentage done
                load = (D(a) / (fileChar))
		load = load * 100
                print("Percent Done: " + str(load))
		print("Characters Processed: " + str(a) + " of " + str(fileChar))
		a = a * -1
	#print the text being encoded to the screen
		payload = fileContents[counter:-a]
		print("Payload: ")
                print(payload)
		qr.add_data(payload)
		qr.make(fit=True)

	#Create the file  and save it
		realname= str(nameCount) + ".tiff"
		location = directoryName + "/" + realname
		img = qr.make_image(fill_color="black", back_color="white")
		img.save(location)


	#adjust variables
		counter += 1500
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
        pattern = "*.tiff"
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
	#Flag for enabling duplicate data checkand removal
	dupFlag = ""
	dupFlag = raw_input("Would you like to enable duplcate value checks? \n Enabling this checks to see if data read has already been \n read in the previous frame y/n: ")
	print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
	#make new file todump data
	f= open("HEXassemble.txt", "a")
	listOfFiles = os.listdir('.')
        pattern = "*.tiff"
	count = 0
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
			print(entry)
			count +=1


	#make cache to prevent duplicates qr
	cache= ""
	duplicate = 0
        i = 0
	while i < count:

		#show amount done
		load = (D(i) / (count))
                load = load * 100
                print("Percent Done: " + str(load))


        	qr = qrtools.QR()
		print("Decoding: " + str(i) + " of " + str(count))
#		file = "image" + str(i)
                file = str(i)

	       	try:
			qr.decode(file + ".tiff")
		except:
			print("read error trying again")
			qr.decode(file + ".tiff")
		#check cache for duplicate 
		if cache != qr.data:
			f.write(qr.data)
			print(file)
			print(qr.data)
		else:
			print("Duplicate Found")
			duplicate += 1
		i += 1
		# add the cache for duplicate checks if option choosen
		if dupFlag == "y":
			cache = qr.data
#		time.sleep(.05)
	print(str(duplicate) + " Duplicates found.")
	f.close()
        Pause()
        return

#function for iterating through list/array
def steps(files,y,frame_array,pathIn):
	global path
	#file file of file names
	list= open("VideoNames.txt","a")
	pathOut= str(path) + ".avi"
	listName = pathOut
	pathOut = "./"  + pathOut
	list.write("file " + listName + "\n")
	list.close
	for n in y:
		filename=pathIn + files[n]
		fps= 2.0
                #reading each files
	        print(filename)
	        img = cv2.imread(filename)
	        height, width, layers = img.shape
	        size = (width,height)
		frame_array.append(img)
                out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

	#for i in range(len(frame_array)):
            # writing to a image array
        for n in y:
	   out.write(frame_array[n])
        out.release()
        print(pathOut+" made!")
	#empty array
	for n in y:
		frame_array[n] = 0 
        print("break")
	#time.sleep(10)
        global x
        x += 10
        if x > len(files):
                x = len(files)
        global b
        b += 10
	path +=1
        return
#MAkes the video bank to be combined
def MMcreate():
	Banner()
	path = raw_input("Enter Folder of QR images to compile: ")
	if path == "":
                return
	path = "./" + path + "/"
	pathIn= path
	frame_array = []
	files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
	#for sorting the file names properly
	files.sort(key = lambda x: x[5:-4])
	files.sort()
	frame_array = []
	files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
	#for sorting the file names properly
	files.sort(key = lambda x: int(filter(str.isdigit, x)))




#	for i in range(len(files)):
#	        filename=pathIn + files[i]
#	        #reading each files
#		print(filename)
#	        img = cv2.imread(filename)
#	        height, width, layers = img.shape
#	        size = (width,height)
#
 #   #inserting the frames into an image array
#	        frame_array.append(img)
#	        out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
#	Pause()


	global b
	global x

	while b < len(files):
		#print("MM make")
		#time.sleep(10)
		y= range(b,x)
		steps(files,y,frame_array,pathIn)
#	for i in range(len(frame_array)):
#	    # writing to a image array
#	    out.write(frame_array[i])
#	out.release()
#	print("video.avi made!")
	Pause()
	return

#Conacate all video clips in a certain folder
def Con():
 
	os.system("ffmpeg -f concat -i VideoNames.txt -codec copy output.avi")
	Pause()
	return


def MMbreak():
	Banner()
	#liost files
	print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
	listOfFiles = os.listdir('.')
        pattern = "*.avi"
	pattern2 = "*.mp4"
        count = 0
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)
                        count +=1
		if fnmatch.fnmatch(entry, pattern2):
                        print(entry)
                        count +=1
	file = raw_input("Enter File name to deconstruct: ")
	#check for empty value
	if file == "":
		return
	vidcap = cv2.VideoCapture(file)
	def getFrame(sec):
	    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
	    hasFrames,image = vidcap.read()
	    if hasFrames:
	        cv2.imwrite(str(count)+".tiff", image)     # save frame as JPG file
	    return hasFrames
	sec = 0
	frameRate = .5 #//it will capture image in each 0.5 second
	count=0
	success = getFrame(sec)
	while success:
	    count = count + 1
	    sec = sec + frameRate
	    sec = round(sec, 2)
	    success = getFrame(sec)

	print("Video Deconstructed!")
	Pause()
	return


#convert reassembled hex file to orginal file type
def Hex2Bi():
	Banner()
	print("----------Working Directory Files ")
        #list files in working directory
        print("Files: ")
        listOfFiles = os.listdir('.')
        pattern = "*.txt"
        for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                        print(entry)
	fileName = raw_input("Enter file you wish to restore: ")
	if fileName == "":
		return
	#OPen file
	with open(fileName, 'rb') as f:
                content = f.read()
        print("HEX data: " + content)
        binary_string = binascii.unhexlify(content)
	exten = raw_input("Enter file type: ")
	new = raw_input("Enter name for restored file: ")

	newFile = open(new, 'a')
	newFile.write(binary_string)
	newFile.close
#	print(binary_string)
	new_filename = Path(new).stem + exten
#	base = os.path.splitext(newFile)[0]
#	os.rename(newFile, base + exten)
	Pause()
	return


########################################################3
#Home Menu
def Home():
	#reset globals
	global x
	global b
	global path
	x = 10
	b = 0
	path = 0
	#List Options
	Banner()
	print("1. Convert file to Hex")
        print("2. Fragment and encode Hex file to bank of QR images")
	print("3. Read indvidual QR image")
	print("4. Reassemble bank of QR images")
	print("5. Assemble video bank from QR bank  ")
	print("6. Assemble full video from video bank")
	print("7. Deconstruct video into QR bank")
        print("8. Restore file")
	print("9. Quit")
        choice = raw_input("Enter Choice: ")
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
			Con()
                if choice == '7':
                        MMbreak()
                if choice == '8':
                        Hex2Bi()
	        if choice == '9':
                        Zip()
                if choice == 'q':
			Banner()
                        quit()
	else:
		Home()
	Home()

Home()

