import datetime
import time
import csv
import os
from yahoo_fin.stock_info import *
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as graph
from matplotlib import style

def realtimechart(symbol):
    ladefrequenz = 15 
    dateiname = "{}.csv".format(symbol)
      
    def dateicheck():
        jetzt = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        existiert = os.path.isfile(dateiname)
        if existiert == False:
            kurs = get_live_price(symbol)
            kurs_jetzt = (jetzt, round(kurs,2))
            with open(dateiname, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(kurs_jetzt)
                f.close()
        else: pass   
     
    def speichern(symbol):
        while (True):
            kurs = get_live_price(symbol)
            time.sleep(ladefrequenz)
            jetzt = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            kurs_jetzt = (jetzt, round(kurs,2))
            with open(dateiname, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(kurs_jetzt)
    
    style.use('dark_background')
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    
    def drucken(i):
        x_array=[]
        y_array=[]
        jetzt = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        with open(dateiname,'r') as csvfile:
            csvFileReader=csv.reader(csvfile)
            next(csvFileReader)
            row1 = next(csvFileReader)
            for row in csvFileReader:
                if (len(row)>0):
                    x_array.append(row[0])
                    y_array.append(float(row[1]))
        ax1.clear()
        plt.title("Kurs {} Stand: {}".format(symbol, jetzt))
        ax1.plot(x_array,y_array)
        ax1.set_ylabel("in jeweiliger Währung", rotation=90, fontsize=10, fontweight='bold')
        ax1.set_xlabel("Vom {} bis {}".format(row1[0],jetzt))
        plt.tight_layout()
        
    dateicheck()
    speichern = threading.Thread(target=speichern, args=(symbol,))
    speichern.daemon = True
    speichern.start()
    darstellung = graph.FuncAnimation(fig, drucken, interval = (ladefrequenz*1000))
    plt.show()
    return darstellung

# call it!

realtimechart = realtimechart("DPW.DE")