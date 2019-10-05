AI: Deep Learning for Email Spam Detection
=======================================


Requirements
------------

This code was created with Python 3.6.7

Using Kaggle Spam-filter database https://www.kaggle.com/karthickveerakumar/spam-filter

Make sure to install all requirements:

    $ pip install -r requirements.txt


Quick start
-----------

Open a separate tab or window and run:

    $ python3 flaskrestapi.py

Now go back to the original tab or window and run:

    $ python3 request.py -e "This is a spam from email@email.com"

    Output:

    $[{'percentage': 57.13035464286804, 'result': 'email is probably spam.'}]


