"""
HESAM MOTLAGH - The Johns Hopkins Univeristy - Hesamnmotlagh@gmail.com
-------------------------------------------------------------------------------
Script name:     AAPL_analysis
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

    

#what data do I want to compare?
#[stock price and volume] vs. [twitter sentiment and twitter volume]

#First let's break down the twitter data into trading hours
raw_dat = open("AAPL_twitter_sent.dat",'r')
lines = raw_dat.readlines()
raw_dat.close()
#we want things from friday back to monday
#monday = 7/13 and firday = 7/17
#trading hours are from 9:30AM-4:30PM
#the tweets are in UTC = 4 hours off of EST
prev_day, day_count = 13, 5
output = open("AAPL_Sent_Day" + str(day_count)+".dat",'w')
for x in range(1,len(lines)+1):
    line = lines[len(lines)-x]
    date = line.split(',')[0]
    if((int(date[4:6]) > 12) and (int(date[4:6]) < 18)):
        #ok we're in the right day of the week, are we occuring during
        #trading hours?
        hour, minute = int(date[7:9])-4, int(date[10:12])
        time = hour*60 + minute
        #ok we're in EST now, are we within trading hours?
        if((time >= (9*60+30)) and (time <= (16*60))):
            #now we're in trading hours!  
            if(int(date[4:6]) != prev_day):
                #we just changed to a new day, need a new output file
                output.close()
                day_count+=1
                output = open("AAPL_Sent_Day" + str(day_count)+".dat",'w')
            output.write(str(hour*60+minute-9*60-30)+","+line.split(',')[1])
            prev_day = int(date[4:6])
output.close()


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)


days = [5,6,7,8,9]
for day in days:

    #ok so it's clear that I want to plot the sentiment data in 15 minute windows
    #first let's grab the stock data
    raw = open("AAPL_Day_" + str(day) + ".dat")
    lines = raw.readlines()
    raw.close()
    
    time, prices, vol = [], [], []
    mintime = int(lines[0].split(',')[0])
    
    for line in lines[1:len(lines)-1]:
        datp = line.split(',')
        time.append(int(datp[0])-mintime)
        prices.append(float(datp[1]))
        vol.append(float(datp[3]))
    
    
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
    
    
    
    fig, ax1 = plt.subplots()
    ax1.plot(time, prices, 'r-')
    ax1.set_xlabel('Minutes Since Market Opened (min)')
    ax1.set_ylabel('Stock Price ($)',color = 'r')
    for tl in ax1.get_yticklabels():
        tl.set_color('r')
    ax2 = ax1.twinx()
    ax2.plot(timeTw,sentTw,'-o')
    ax2.set_ylabel('Twitter Sentiment (A.u.)', color = 'b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    
    pp = PdfPages('Day'+str(day)+'price_v_sent.pdf')
    plt.savefig(pp,format='pdf')
    pp.close()
    
    plt.cla()
    plt.clf()
    plt.close()
    fig, ax1 = plt.subplots()
    ax1.plot(time, prices, 'r-')
    ax1.set_xlabel('Minutes Since Market Opened (min)')
    ax1.set_ylabel('Stock Price ($)',color = 'r')
    for tl in ax1.get_yticklabels():
        tl.set_color('r')
    ax2 = ax1.twinx()
    ax2.plot(timeTw,volTw,'-o')
    ax2.set_ylabel('Tweet Volume (# Tweets)', color = 'b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    
    
    pp = PdfPages('Day'+str(day)+'price_v_vol.pdf')
    plt.savefig(pp,format='pdf')
    pp.close()
    
    
    
    
    
    fig, ax1 = plt.subplots()
    ax1.plot(time, vol, 'r-')
    ax1.set_xlabel('Minutes Since Market Opened (min)')
    ax1.set_ylabel('Volume Traded (# shares)',color = 'r')
    for tl in ax1.get_yticklabels():
        tl.set_color('r')
    ax2 = ax1.twinx()
    ax2.plot(timeTw,sentTw,'-o')
    ax2.set_ylabel('Twitter Sentiment (A.u.)', color = 'b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    
    pp = PdfPages('Day'+str(day)+'vol_v_sent.pdf')
    plt.savefig(pp,format='pdf')
    pp.close()
    
    plt.cla()
    plt.clf()
    plt.close()
    fig, ax1 = plt.subplots()
    ax1.plot(time, vol, 'r-')
    ax1.set_xlabel('Minutes Since Market Opened (min)')
    ax1.set_ylabel('Volume Traded (# shares)',color = 'r')
    for tl in ax1.get_yticklabels():
        tl.set_color('r')
    ax2 = ax1.twinx()
    ax2.plot(timeTw,volTw,'-o')
    ax2.set_ylabel('Tweet Volume (# Tweets)', color = 'b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    
    
    pp = PdfPages('Day'+str(day)+'vol_v_vol.pdf')
    plt.savefig(pp,format='pdf')
    pp.close()
