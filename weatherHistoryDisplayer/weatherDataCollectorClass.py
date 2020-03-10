# Name = Erik V.
# Student number = 221122
import xml.etree.ElementTree as ET
import urllib.request
from time import sleep
from datetime import datetime
count = 0
    
class dataCollector:
    
    def __getXmlTree__(url):
        """Will return the XML tree made with the url given"""
    
        # Getting the data from the url
        with urllib.request.urlopen(url) as url:
        
            data = url.read()
    
        # Making a tree with the data
        tree = ET.fromstring(data)
        return tree

    def __getXmlInfoInDic__():  
        """Will return the info at the id in a dictionary"""
       
        # Leeuwarden = 6270 Groningen 6280
        # Getting the XML tree from the url
        tree = dataCollector.__getXmlTree__("https://data.buienradar.nl/1.0/feed/xml")

        # Getting the info for the current ID (leeuwarden)
        node = tree.findall('''.//*[@id='6270']''')[0]
    
        # Making a dictionary to store the data in
        weatherDic = {}

        for element in node.iter():

            weatherDic.update({element.tag : element.text})

        return weatherDic

    def __saveData__(weatherDic):
        """Will save the data from the dictionary to the file"""
        global count

        filename = "C:\\Users\\Erik Veenstra\\source\\repos\\weatherHistoryDisplayer\\weatherHistoryDisplayer\\weatherDataCollection.txt"

        file = open(filename, "a+")

        saveCurrentDataEntry = True

        theTime = ""

        if (saveCurrentDataEntry):
            
            for key, value in weatherDic.items():

                if not (key == "weerstation"):

                    file.write("{} : {}\n".format(key, value))

            file.write("###\n")

            file.close()
            currentTime = datetime.now().strftime("%H:%M")
            count += 1
            print("Weather data collection number {} at {} completed".format(count, currentTime)) 

        else:

            currentTime = datetime.now().strftime("%H:%M")
            print("current time {} not saved time = {}".format(currentTime, theTime))

    def startDataCollection(secondsInterval):
                
        # Saving the data every x seconds
        while True:
            
            # Getting a dictionary filled with the weather data 
            weatherDic = dataCollector.__getXmlInfoInDic__()   
        
            # Saving the data to the file
            dataCollector.__saveData__(weatherDic)

            # Letting the program sleep for x seconds before repeating
            sleep(secondsInterval)               