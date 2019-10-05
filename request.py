#!/usr/bin/env python
"""
This file will make a simple request to the Flask API for email processing.
""" 
import argparse
import requests
import datetime
import email
import imaplib
import mailbox
import numpy as np
import re 
import os

def create_filter(email_from, x):
    directory = "filters"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = "filter_" + str(x) + ".xml"
    file = "filters/" + file_name
    output_file = open(file, 'w')
    output_file.write("""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <title>Mail Filters</title>
    <id>tag:mail.google.com,2008:filters:z0000001570292617973*4877144193510239052</id>
    <updated>2019-10-05T09:22:37Z</updated>
    <author>
        <name>Alexandru Badea</name>
        <email>coralexbadea99@gmail.com</email>
    </author>
    <entry>
        <category term='filter'></category>
        <title>Mail Filter</title>
        <id>tag:mail.google.com,2008:filter:z0000001570292617973*4877144193510239052</id>
        <updated>2019-10-05T09:22:37Z</updated>
        <content></content>
        <apps:property name='from' value="%s"/>
        <apps:property name='shouldArchive' value='true'/>
        <apps:property name='sizeOperator' value='s_sl'/>
        <apps:property name='sizeUnit' value='s_smb'/>
    </entry>
</feed>""" %(email_from[0]))


def main(account, password, num_emails = "3", email_type = "ALL"):


     # Define URL for Flask API endpoint.
    KERAS_REST_API_URL = "http://127.0.0.1:45000/predict"
    
    black_email_list = []

    #connect to the gmail account
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(account, password)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, email_type) # (ALL/UNSEEN)
    i = len(data[0].split()) #total number of emails




    for x in range(i-1, i - int(num_emails), -1):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        try:
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
        except:
            continue
        
        # Header Details
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
     

        # Body details
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                #form bytes to string
                body = body.decode('utf8')
               
                # Set the payload to JSON format.
                payload = {"email": body, "from":email_from}
                

                # Submit the request.
                r = requests.get(KERAS_REST_API_URL, json=payload)

                response = r.json()

                print(response)
                if(response[0]["percentage"] > 50):
                    email_from = re.findall("\<(.*?)\>", email_from)
                
                    create_filter(email_from, x)

            else:
                continue

      
        # Ensure the request was sucessful.
        #if response["success"]:
                # Loop over the predictions and display them.
         #       print(response['predictions'])

        # Otherwise, the request failed.
        #else:
         #       print("Request failed")
    print(black_email_list)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Purple rain')
    parser.add_argument(
        '-a',
        dest='account',
        action='store',
        required=True,
        help="This is the gmail account name."
    )
    parser.add_argument(
        '-p',
        dest='password',
        action='store',
        required=True,
        help="This is the gmail passoword"
    )
    parser.add_argument(
        '-n',
        dest='num_emails',
        action='store',
        required=False,
        
        help="Number of emails to iterate through"
    )
    parser.add_argument(
        '-t',
        dest='email_type',
        action='store',
        required=False,
        help="What emails we want to check(ALL/UNSEEN)."
    )

    args = parser.parse_args()

    main(**vars(args))


