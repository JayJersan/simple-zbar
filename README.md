# simple-zbar
A barcode reader that takes video from webcam and shows customizable popups for barcodes and QR codes with optionally additional data

# Usage
You can start scanning barcodes/QR codes supported by zbar without any configuration. If you want to scan only a specific type(s) of barcode, you can change the arguments for zbar in [simple-zbar.py](/simple-zbar/simple-zbar.py)
Every time the code is run, a csv file is created that logs all the barcodes scanned with the data in [Data.csv](simple-zbar/Data.csv) if applicable for the session
After you feel like you have scanned enough, press q to quit

#Customization
To change the pop-ups, modify the [Data.csv](simple-zbar/Data.csv) file
  * The first column matches with the barcode scanned
  * Leave the label for the second column. The timestamp will be inserted automatically
  * Add or modify the remaining labels as you want!
 
Now, you can add some entries into the file and the pop-up will show the data
