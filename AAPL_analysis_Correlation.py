"""
HESAM MOTLAGH - The Johns Hopkins Univeristy - Hesamnmotlagh@gmail.com
-------------------------------------------------------------------------------
Script name:     AAPL_analysis_Correlation 
First written:   2015.07.19
Last edited:     2015.07.20

Purpose:
The script was written by Hesam Motlagh to plot the stock data versus the 
twitter sentiment data.
"""

import sys, math, os, string, csv #import other stuff we need
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

    

output = open("Correlations.dat",'w')
days = [5,6,7,8,9]
for day in days:
    #day = 5
    #ok so it's clear that I want to plot the sentiment data in 15 minute windows
    #first let's grab the stock data
    raw = open("AAPL_Day_" + str(day) + ".dat")
    lines = raw.readlines()
    raw.close()
    
    time, prices, volume, psum,vsum = [], [], [], [], []
    mintime = int(lines[0].split(',')[0])
    prev_time = 0
    
    for line in lines[1:len(lines)-1]:
        datp = line.split(',')
        tval = int(datp[0])-mintime
        if(tval/15 != prev_time):
            #finished 15 minute window
            psumnp = np.array(psum)
            vsumnp = np.array(vsum)
            prices.append(psumnp.mean())
            volume.append(vsumnp.mean())
            time.append(float(prev_time*15.0 + 7.5))
            psum, vsum = [], []
            prev_time += 1
        psum.append(float(datp[1]))
        vsum.append(float(datp[3]))
    
    
    
    
    #now let's bring in the twitter data and average it over 15 minute windows
    file_to_open = open("AAPL_Sent_Day"+str(day)+".dat",'r')
    lines = file_to_open.readlines()
    file_to_open.close()
    
    prev_time, curr_vol, sum_val = 0, 0, 0
    timeTw, sentTw, volTw = [], [], []
    to_write = ""
    for line in lines:
        curr_vol += 1
        if(int(line.split(',')[0])/15 != prev_time):
            timeTw.append(float(prev_time*15.0 + 7.5))
            sentTw.append(float(sum_val)/float(curr_vol))
            volTw.append(curr_vol)
            sum_val, curr_vol, sum_val = 0, 0, 0
            prev_time+=1
        sum_val += float(line.split(',')[1])
        
        #to_write += line.split(',')[1].strip('\n')+"\t"
    
    data = [[prices,"Price"], [volume,"Vol"], \
            [sentTw,"Sentiment"], [volTw,"VoluTw"]]
    f, multi = plt.subplots(len(data),len(data))
    
    for s1 in range(0,len(data)):
        for s2 in range(0,len(data)):
                x_val = data[s1][0]
                y_val = data[s2][0]
                if(len(y_val) > len(x_val)):
                    #off by one error
                    y_val = y_val[0:len(y_val)-1]
                if(len(y_val) < len(x_val)):
                    #off by one error
                    x_val = x_val[0:len(x_val)-1]
                slope,intercept,r_val,p_val,std_err = stats.linregress(x_val,y_val)
                min_x = min(x_val)
                max_x = max(x_val)
                x_vals = np.linspace(min_x,max_x,100)
        
                multi[s1,s2].plot(x_vals,x_vals*slope + intercept)
                multi[s1,s2].scatter(x_val,y_val)
                multi[s1,s2].set_title(data[s1][1] + " vs. " + data[s2][1])
                
                output.write("Day " + str(day))
                output.write( data[s1][1] + " vs. " + data[s2][1] + "\n")
                output.write( "R   = " + str(r_val) + "\n")
                output.write( "R^2 = " + str(r_val*r_val) + "\n" )
                output.write( "-------------------------------------\\nn" )
    
    pp = PdfPages('Day'+str(day)+'corr_plot.pdf')
    plt.savefig(pp,format='pdf')
    pp.close()

output.close()
