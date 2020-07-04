AI: Deep Learning for Email Spam Detection
=======================================

Overview
------------
Using Kaggle Spam-filter database https://www.kaggle.com/karthickveerakumar/spam-filter

This program uses flask API for keeping the model on server, then every request sends the email to be classified as spam or not spam.
The server response gives the percentage on an email being a spam and also who send it.
Then the program creates filters in xml format for gmail with the spam email adresses.
The filters can be used for Gmail

Requirements
------------

This code was created with Python 3.6.7


Enable imap usage in gmail account from Settings -> Forwarding and POP/IMAP

Also activate the permission for less secure apps from https://myaccount.google.com/lesssecureapps?pli=1

Make sure to install all requirements:

    $ pip install -r requirements.txt


Quick start
-----------

Run the flask server:

    $ python3 flaskrestapi.py

Perform a request for your account:
    
    $  python3 request.py -a <ACCOUNTNAME> -p <PASSWORD> -n 10 -t ALL 

    
    Output:

    $[{'from': 'The Nincha Team <hello@ninchanese.com>', 'percentage': 82.88823962211609, 'result': 'email is probably spam.'}]
    [{'from': 'Quora Digest <digest-noreply@quora.com>', 'percentage': 17.186427116394043, 'result': 'email is probably not spam.'}]
    [{'from': 'Alexandru Badea <coralexbadea99@gmail.com>', 'percentage': 49.49015974998474, 'result': 'email is probably not spam.'}]
    [{'from': '"Medium Daily Digest" <noreply@medium.com>', 'percentage': 99.30974841117859, 'result': 'email is probably spam.'}]
    [{'from': 'The Nincha Team <hello@ninchanese.com>', 'percentage': 82.88823962211609, 'result': 'email is probably spam.'}]
    [{'from': 'YouTube <noreply@youtube.com>', 'percentage': 72.70362973213196, 'result': 'email is probably spam.'}]

    Type:
       python request.py -h 
    for help
