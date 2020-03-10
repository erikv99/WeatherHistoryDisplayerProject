# Name = Erik Veenstra
# Student number = 221122
import threading
import weatherDataCollectorClass as WDC
import weatherDataGUIClass as WDG
from datetime import datetime

def main():

    # Starting the collection of data with a 10 minute interval (data gets saved to a file)
    # All the data collections that arent on 20m 40m or 00m will get filtered out.
    # trying every 10m now, so we gather data every 5
    thread1 = threading.Thread(target=WDC.dataCollector.startDataCollection, args=(300,))
    currentDate = datetime.now().strftime("%d/%m/%Y")
    thread2 = threading.Thread(target=WDG.guiClass.drawMainWindow, args=(currentDate,))
    thread1.start()
    thread2.start()

if (__name__ == "__main__"):

    main()

# todo: plot will only be drawn if the plot has 2 valid data entrys 