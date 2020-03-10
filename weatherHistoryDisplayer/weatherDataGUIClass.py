import tkinter as tkin
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as md
import numpy as np
import datetime

class guiClass:
    """Class for handling the gui part of the program"""

    def __getData__():
        """Function will get a list of dictionarys each containing 1 data entry"""
        file = open("C:\\Users\\Erik Veenstra\\source\\repos\\weatherHistoryDisplayer\\weatherHistoryDisplayer\\weatherDataCollection.txt")
    
        # List of dictionarys that each have 1 data collection.
        listOfDictionarys = []
        currentDic = {}
        
        for line in file:
    
            line = line.replace("\n", "")
        
            # If we find our marker that its the end of this data collection report
            if ("###" in line):
        
                # Adding this dic of data to our list of dictionarys
                listOfDictionarys.append(currentDic)

                # Clearing the current dic so we can put new data in it
                currentDic = {}

            else:
        
                key, val = line.split(":", 1)
                currentDic.update({key : val})

        return listOfDictionarys

    def __getX__(fromDate, toDate):
        """Will return the x values in a list of datetime objects for the time for the plot """
        # X value will be time nearly always
        # From / to date must be in following formate dd/mm/yyyy
        listOfDictionarys = guiClass.__getData__()
        xValues = []

        # Getting the from date and to date
        try:

            fromDay, fromMonth, fromYear = fromDate.split("/")
            toDay, toMonth, toYear = toDate.split("/")
            fromDay, fromMonth, fromYear, toDay, toMonth, toYear = int(fromDay), int(fromMonth), int(fromYear), int(toDay), int(toMonth), int(toYear)

        except(ValueError, TypeError):

            print("Error: weatherDataGUIClass error in line 58!")

        # Looping thru all the dicitionarys
        for i in range(len(listOfDictionarys)):
            
            # Getting the current dictionary
            curDic = listOfDictionarys[i]

            # Looping thru every key and value
            for key, value in curDic.items():

                if (key == "datum "):

                    # Getting the date and time from the dictionary
                    theDate, theTime = value.split()
                    month, day, year = theDate.split("/")
                    hour, minute, second = theTime.split(":")
                    month, day, year = int(month), int(day), int(year)
                    hour, minute, second = int(hour), int(minute), int(second)

                    fromDateCorrect = False
                    toDateCorrect = False

                    if (month >= fromMonth and year >= fromYear):

                        # If the months are the same we have to check the day
                        if (month == fromMonth):

                            if (fromDay <= day):

                                fromDateCorrect = True

                        else:

                            fromDateCorrect = True

                    if (month <= toMonth and year <= toYear):
                            
                        # If the months are the same we have to check the days
                        if (month == toMonth):
                            
                            if (day <= toDay):

                                toDateCorrect = True
                        
                        else:
                            
                            toDateCorrect = True
        
                    if (fromDateCorrect and toDateCorrect):

                        xValues.append(datetime.datetime(year, month, day, hour, minute))
        return xValues

    def __getY__(keyName, fromDate, toDate):
        """Will return the y values for a certain value (example: Temperature) (name must be same as in the dic)"""

        listOfDictionarys = guiClass.__getData__()
        yValues = []

        # Getting the from date and to date
        try:

            fromDay, fromMonth, fromYear = fromDate.split("/")
            toDay, toMonth, toYear = toDate.split("/")
            fromDay, fromMonth, fromYear, toDay, toMonth, toYear = int(fromDay), int(fromMonth), int(fromYear), int(toDay), int(toMonth), int(toYear)

        except(ValueError, TypeError):

            print("Error: weatherDataGUIClass error in line 129!")

        # Looping thru all the dicitionarys
        for i in range(len(listOfDictionarys)):
            
            # Getting the current dictionary
            curDic = listOfDictionarys[i]

            # Looping thru every key and value and getting the date
            for key, value in curDic.items():

                if (key == "datum "):

                    # Getting the date and time from the dictionary
                    theDate, theTime = value.split()
                    month, day, year = theDate.split("/")
                    month, day, year = int(month), int(day), int(year)

            for key, value in curDic.items():

                if (key == keyName):

                    fromDateCorrect = False
                    toDateCorrect = False

                    if (month >= fromMonth and year >= fromYear):
                        
                        # If the months are the same we have to check the day
                        if (month == fromMonth):
                        
                            if (fromDay <= day):
                            
                                fromDateCorrect = True
                        else:
                            
                            fromDateCorrect = True
                    
                    if (month <= toMonth and year <= toYear):                      
                    
                        # If the months are the same we have to check the days
                        if (month == toMonth):                           
                        
                            if (day <= toDay):
                            
                                toDateCorrect = True                        
                        else:                            
                            
                            toDateCorrect = True
        
                    if (fromDateCorrect and toDateCorrect):

                        try:

                            val = float(value)
                            yValues.append(val)

                        except(ValueError, TypeError):

                            print("ValueError or TypeError")

        return yValues

    def __drawPlotWidget__(root, valueName, yAxisLabel, title, date):
        """Will create the right plot and put it in a widget that can be placed and returns it"""
        
        # Selecting the figure type
        fig, ax = plt.subplots(1, 1)

        # We auto get the values for the currentDate
        xValues = np.array(guiClass.__getX__(date, date))
        yValues = np.array(guiClass.__getY__(valueName, date, date))
        
        plt.xlabel("Tijd")
        plt.ylabel(yAxisLabel)

        # If the one of the value arrays only has 1 or 0 entrys it will not work
        if (xValues.size < 2 or yValues.size < 2):

            xValues = [1,2,3,4]
            yValues = [1,2,3,4]
            plt.xlabel("No data found for this date!")

        day, month, year = date.split("/")

        plt.title(title + " ({}/{})".format(day, month))

        plt.plot(xValues, yValues) # X values, Y values

        # Set time format and the interval of ticks (every 20 minutes)
        xformatter = md.DateFormatter('%H:%M')
        xlocator = md.MinuteLocator(byminute = [0, 20, 40], interval = 1)

        # Set xtick labels to appear every 20 minutes
        ax.xaxis.set_major_locator(xlocator)

        # Format xtick labels as HH:MM
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        
        # Rotating the timestamps so they dont overlap
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=90)

        canvas = FigureCanvasTkAgg(fig, master=root)
        plotWidget = canvas.get_tk_widget()
        plotWidget.grid(row=0, column=0, columnspan=4, sticky=tkin.N+tkin.S+tkin.E+tkin.W)
        plotWidget.columnconfigure(0, weight=1)
    
    def refresh(firstRoot, entry):
        """Function will refresh the window and the stats"""
        
        input = entry.get()
        inputValid = guiClass.checkDateInput(input)
        
        if (inputValid):

            firstRoot.destroy()
            guiClass.drawMainWindow(input)

        else:

            #tkinter pop up msg here
            tkin.messagebox.showerror("Error", "Input is not in the right format. Format should be DD/MM/YYYY")

    def checkDateInput(entry):
        """Will return true if entry is correct, false if not"""
        try:

            a, b, c = entry.split("/")

            if (a.isdigit() and b.isdigit() and c.isdigit()):

                    return True

            else:

                return False

        except(ValueError, TypeError):

            return False     


    def drawMainWindow(ddate):
        """Will draw the main window"""

        # Getting our root window in tkinter
        root = tkin.Tk()
        root.columnconfigure(0, weight=1)
        root.title("Weer Geschiedenis Weergever")
        root.geometry("670x580")

        # Drawing the plot already so it looks ok from the start
        guiClass.__drawPlotWidget__(root, "temperatuurGC ", "Graden Celsius", "Graden Celsius", ddate)

        # Making and placing the buttons
        but1 = tkin.Button(root, text="Graden Celsius", command= lambda : guiClass.__drawPlotWidget__(root, "temperatuurGC ", "Graden Celsius", "Graden Celsius", ddate), width=20, height=2, padx=5, pady=5)
        but2 = tkin.Button(root, text="Luchtvochtigheid", command= lambda : guiClass.__drawPlotWidget__(root, "luchtvochtigheid ", "Luchtvochtigheid in %", "Luchtvochtigheid", ddate), width=20, height=2, padx=5, pady=5)
        but3 = tkin.Button(root, text="Graden Celsius 10CM", command= lambda : guiClass.__drawPlotWidget__(root, "temperatuur10cm ", "Graden Celsius 10CM", "Graden celsius 10cm boven de grond", ddate), width=20, height=2, padx=5, pady=5)
        but4 = tkin.Button(root, text="Zicht meters", command= lambda : guiClass.__drawPlotWidget__(root, "zichtmeters ", "Zichtmeters", "Zichtmeters", ddate), width=20, height=2, padx=5, pady=5)
        but1.grid(row=1, column=0, columnspan=1, sticky=tkin.N+tkin.S+tkin.E+tkin.W)
        but2.grid(row=1, column=1, columnspan=1, sticky=tkin.N+tkin.S+tkin.E+tkin.W)
        but3.grid(row=1, column=2, columnspan=1, sticky=tkin.N+tkin.S+tkin.E+tkin.W)
        but4.grid(row=1, column=3, columnspan=1, sticky=tkin.N+tkin.S+tkin.E+tkin.W)
        
        # Making the date entry box and label and placing them
        labelText = tkin.StringVar()
        labelText.set("Voer datum in voor de weer geschiedenis:")
        label = tkin.Label(root, textvariable=labelText)
        label.grid(row=2, column=0, columnspan=2, sticky=tkin.E)

        entry = tkin.Entry(root)
        entry.insert(0, ddate)
        entry.grid(row=2, column=2, sticky=tkin.W, padx=5)

        refreshButton = tkin.Button(root, text="Haal op", command= lambda : guiClass.refresh(root, entry), width = 20, height = 2)
        refreshButton.grid(row=2, column=3, sticky=tkin.E, padx=25, pady=10)
        root.mainloop()
        
