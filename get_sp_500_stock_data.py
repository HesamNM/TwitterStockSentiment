"""
HESAM MOTLAGH - The Johns Hopkins Univeristy - Hesamnmotlagh@gmail.com
-------------------------------------------------------------------------------
Script name:     get_sp_500_stock_data.py
First written:   2015.07.18
Last edited:     2015.07.18

Purpose:
The script was written by Hesam Motlagh to scrape per minute data from google
finance and save it as data that can be plotted easily.
"""

#import beautifulsoup
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import requests, urllib2, time


def get_data(ticker):
    url_temp = "http://www.google.com/finance/getprices?i=60&p=10d&f=d,o,h,l,c,v&df=cpct&q="
    #ticker is a string
    url = url_temp + ticker
    page = urllib2.urlopen(url)
    page_content = page.readlines()
    
    data, dat_start, min_count, po = [], False, 0, 0.0
    for line in page_content:
        if(line.split(',')[0][0] == 'a'):
            dat_start = True
            if(min_count == 0):
                po = float(line.split(',')[4])
        if(dat_start):
            if(line.split(',')[0][0] != 'a'):
                min_count += 1
                point = line.split(',')
                data.append([min_count,float(point[1]),(float(point[1])-po)/po*100,\
                    float(point[5])])
    return data
    
    
raw = open('s_p_500.dat','r')
lines = raw.readlines()
raw.close()
all_data = []
for name in lines[0].split(','):
    temp_dat = get_data(name)
    print name
    time, ret = [], []
    for x in temp_dat:
        time.append(float(x[0]))
        ret.append(float(x[2]))
    plt.scatter(time,ret)
    plt.plot(time,ret)


pp = PdfPages('data.pdf')
#plt.show()
plt.savefig(pp,format='pdf')
plt.savefig('data.png',dpi=600)
pp.close()
            
