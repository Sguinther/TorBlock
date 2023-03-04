#!/bin/python

from flask import Flask, render_template, request, redirect
import requests
#import json
import sqlite3
#import re


torIPs = "https://www.dan.me.uk/torlist/?exit"
torIPs2 = "https://udger.com/resources/ip-list/tor_exit_node"
torIPs3 = "https://lists.fissionrelays.net/tor/exits.txt"
weblist = []

#excludedNodes = ['2.58.56.101', '2.58.56.106', '2.58.56.212', '5.2.67.226', '5.2.70.140']



app = Flask(__name__)

##########################################################################################################################
def getTorIp():
    
    '''
    This function grabs TOR node lists from the web and writes them to a local file. 
    From there, this local file parses the data into list format as strings. 
    This allows us to create a list of all ips from the web and a list of IP data that
    has been pulled from our sqlite3 database using the sqlite3 module. The data lists are run against each other
    and only IPs that have not been manually excluded are shown. 
    '''
    #define DB connection
    connection = sqlite3.connect("ip_addresses.db", check_same_thread=False)
    c = connection.cursor()
    nonexcludedIPs = []
    '''
    #THIS SECTION READS THE IP LIST FROM THE ONLINE SOURCE AND 
    # WRITES IT TO A LOCAL FILE FOR FURTHER USE
    response = requests.request("GET", torIPs3).text
    print(response)
    with open("ips.txt", "w") as f:
        f.write(response)
    '''
    

    #THIS NEXT SECTION PARSES THE IPs INTO AN EASIER TO USE FORMAT (List manipulation)
    with open("ips.txt", 'r') as f:
        weblist = f.read().splitlines()
    #print(ourlist)
    
    #This block of code takes the IPs in the database and runs them against the ones pulled from the web.
    c.execute("SELECT * FROM ip_addr")
    data = c.fetchall()
    ipdata = []
    for entry in data:
        ipdata.append(entry[1])
    for ip in weblist: 
        if ip in ipdata:
            pass
        else:
            nonexcludedIPs.append(ip)
    return nonexcludedIPs, ipdata
##########################################################################################################################


##########################################################################################################################
#This function connects to the database defined above and INSERTs the ip address provided by 
# the end user in the code following this function #This block also connects to the sqlite3 database in the same directory as this file and 
# creates the necessary database if it is not already created
@app.route('/add_ip', methods=['POST'])
def add_ip():
    connection = sqlite3.connect("ip_addresses.db", check_same_thread=False)
    c = connection.cursor()
    ip_address = request.form['ip_address']
    c.execute('''CREATE TABLE IF NOT EXISTS ip_addr
             (id INTEGER PRIMARY KEY, ip_address TEXT)''')
    connection.commit()
    #regex input validation for posted ip
    c.execute('SELECT ip_address FROM ip_addr WHERE ip_address = ?', (ip_address,))
    result = c.fetchone()
    if result is None: 
        c.execute('INSERT INTO ip_addr (ip_address) VALUES (?)', (ip_address,))
        connection.commit()
        connection.close()
        return redirect('/')
    else:
        return redirect('/')

#This one deletes
@app.route('/delete_ip', methods=['POST'])
def delete_ip():
    connection = sqlite3.connect("ip_addresses.db", check_same_thread=False)
    c = connection.cursor()
    ip_address = request.form['ip_address']
    #regex input validation for posted ip
    c.execute('DELETE FROM ip_addr WHERE ip_address = ?', (ip_address,))
    connection.commit()
    connection.close()
    return redirect('/')
##########################################################################################################################


@app.route("/")
def home():

    ips, ips1 = getTorIp()
    
    return render_template('home.html', ips = ips, ips1 = ips1)

app.run(host="0.0.0.0", port = 5000)



