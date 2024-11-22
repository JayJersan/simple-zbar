# Import the required toolkit
from imutils.video import VideoStream
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
from tkinter import *
from tkinter import ttk
from datetime import date
from threading import Thread
from playsound import playsound
import argparse
import datetime
import imutils
import time
import cv2
import csv

# Create popup boxes that close automatically as threads to call as necessary
barcodeData = 'data'
barcodeType= 'type'
def ui(barcodeData, barcodeType):
    root=Tk()
# Code to position window at center of screen
    w=500
    h=150
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
# Elements in popup window
    root.title("Barcode Decoded!")
    data=Label(root, text="Barcode Data:", font=("Segoe UI", 25)).grid(row=0, column=0)
    e1=Label(root, text=barcodeData, font=("Segoe UI", 25)).grid(row=0, column=1)
    typedata=Label(root, text="Standard:", font=("Segoe UI", 25)).grid(row=2, column=0)
    e2=Label(root, text=barcodeType, font=("Segoe UI", 25)).grid(row=2, column=1)
    root.after(5000,lambda:root.destroy())
    root.mainloop()
# Creating thread as a daemon
Thread(target=ui, args=(barcodeData, barcodeType)).daemon = True
# Create a parameter parser to parse parameters
ap = argparse.ArgumentParser()
today = str(time.strftime("%Y-%m-%d_%H-%M"))
ap.add_argument("-o", "--output", type=str, default="barcodes_"+today+".csv",
 help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
# Initialize the video stream to warm up the camera
print("Starting BARCODE SCANNER AND DETAILS VIEWER By Jerwin J...")
print("[INFO] Starting video stream...")
print("[NOTICE] Press q to quit")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#Open file to read data from and store them in array
rows = []
item = []
with open("Data.csv", mode='r') as master:
    csvreader = csv.reader(master)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
# Open the output CSV file to write and initialize all barcodes found so far
found = set()
csv = open(args["output"], "w")
header1 = str(header)
header1 = header1.translate({ord(c):None for c in '\'\]' })
csv.write(str(header1[1:])+"\n")
def det(header, entry):
    details=Tk()
# Code to position window at center of screen
    w=1000
    h=300
    ws = details.winfo_screenwidth()
    hs = details.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    details.geometry('%dx%d+%d+%d' % (w, h, x, y))
    details.title("Barcode Decoded!")
    i=0#data field
    j=1#column position
    c=1#column position refreshing variable
    r=1#row position
#Code to display details fetched from file for the barcode
    for fields in header:
        data=Label
        field=Label
        data=Label(details, text=header[i]+":", font=("Segoe UI", 25)).grid(row=r, column=j)
        field=Label(details, text=entry[i], font=("Segoe UI", 25)).grid(row=r, column=j+1)
        i+=1
        if c%2 == 0:
            r+=1
            j=1
        else:
            j=3
        c+=1
    details.after(5000,lambda:details.destroy())
    details.mainloop()
flag = FALSE
#flag = TRUE
#Ignore above comment
# Loop frames from video stream
while True:
 # Grab frames from a single threaded video stream, 
 # Resize to a maximum width of 400 pixels
 frame = vs.read()
 frame = imutils.resize(frame, width=400)

 # Find the barcodes in the video and parse all barcodes. Remove the symbols argument to parse all barcodes spported by zbar
 barcodes = pyzbar.decode(frame,symbols=[ZBarSymbol.CODE128, ZBarSymbol.EAN13, ZBarSymbol.EAN8, ZBarSymbol.I25,ZBarSymbol.ISBN10, ZBarSymbol.ISBN13, ZBarSymbol.NONE, ZBarSymbol.QRCODE, ZBarSymbol.UPCA])
 # Cycle detected barcodes
 for barcode in barcodes:
  # Extract the bounding box position of the barcode
  # Draw a bounding box around the barcode on the image
  (x, y, w, h) = barcode.rect
  cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

  # Bar code data is a byte object, so if we want to draw it
  # You need to convert it into a string first
  barcodeData = barcode.data.decode("utf-8")
  barcodeType = barcode.type
  # Draw the barcode data and type on the image
  text = "{} ({})".format(barcodeData, barcodeType)
  cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

  # If the barcode text is not currently in the CSV file, write
  # Time stamp + barcode to disk and update the set
  if barcodeData not in found:
#   UI(barcodeData, barcodeType)
   
   for item in rows:
       if barcodeData in item:
           entry = item
           entry.insert(1,str(time.strftime("%Y-%m-%d_%H:%M:%S")))
           entry1 = str(entry)
           entry1 = entry1.translate({ord(c):None for c in '\'\]'})
           csv.write(str(entry1[1:])+"\n")
           csv.flush()
           flag = True
           Thread(target=det, args=(header, entry)).start()
           break
   if (flag == False):
        csv.write("{},{}\n".format(barcodeData, time.strftime("%Y-%m-%d_%H:%M:%S")))
        csv.flush()
        Thread(target=ui, args=(barcodeData, barcodeType)).start()
   found.add(barcodeData)
   playsound('Audio/Beep.mp3')
   flag = False
   # Display output frame
 cv2.imshow("Barcode Scanner", frame)
 key = cv2.waitKey(1) & 0xFF

 # If the "q" key is pressed, the cycle stops
 if key == ord("q"):
  break

# Close the output CSV file for cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
