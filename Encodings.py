#!/usr/bin/env python
import cv2
import face_recognition
import os
import glob
import shutil


src_dir= r'C:\xampp\htdocs\myProject\newImages'
dst_dir= r'C:\xampp\htdocs\myProject\imageAttendance'
for jpgfile in glob.iglob(os.path.join(src_dir,"*.jpg")):
    shutil.copy(jpgfile , dst_dir)                         #copying the image present in newImage folder to imageAttendance folder

images=[]
classnames=[]
path='newImages'
myList=os.listdir(path)

for cls in myList:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classnames.append(os.path.splitext(cls)[0])

def findencodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown=findencodings(images)   #encodeListKnown is a list of lists

with open("encoding.txt", "a") as f:  #if new student registeres his encoding value will be appended in the encoding text file
    for i in encodeListKnown:
       for k in i:
         f.write(str(k)+"\n")


for file in os.listdir(src_dir):
    file_path=os.path.join(src_dir,file)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)   #deleting the image from newImage folder so that there is no duplicate encoding in the text file when next student is registered
    except Exception as e:
        print("")