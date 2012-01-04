# Day 4: Text Processing

## Overview

Today we will discuss text processing.  Our exercises will be grounded in an email dataset (either yours or Kenneth Lay's).  After today, you will be able to compute the most important terms in a particular email, find emails similar to the one you are reading, and find people that tend to send you similar emails.

The techniques will include

* [Tf-Idf](http://en.wikipedia.org/wiki/Tfidf)
* [N-gram](http://en.wikipedia.org/wiki/N-gram)
* [Cosine Similarity](http://en.wikipedia.org/wiki/Cosine_similarity)


## Setting Up

### Datasets


#### 1. Your Own Email

We have provided a [script]() that you can use to download your email.  However before you can run it, you will need to install the following python modules:

* [dateutil]()
* [pyparsing]()

You can now run the script using the following command:

    python download_emails.py [IMAP ADDRESS]

You can pass the optional imap address parameter, otherwise it will default to gmail's imap address.  The script will then ask you to input your email and password, then create the folder `email_root/` and download your email folders into that directory.

#### 2. Kenneth Lay's Emails

Alternatively, if you would rather not use your own emails, or could not get the script working, you can download and unzip Kenneth Lay's  (Pre-bankruptcy Enron CEO) emails that were made public after the accounting fraud scandal.

[Download the emails]()

### Reading Email Files

You will need some code to parse and read the emails.  `email_root` contains a bunch of folders like `_sent` (sent folder), `inbox`, and other folders depending how Kenneth or you organized your emails.  Each folder contains a list of files.  Each file corresponds to a single email.

We have written a module that makes it easier to manage the emails.  To use it add the following import

    import sys
    sys.path.append('PATHTODATAIAP/resources/util/')
    import email_util

The module contains two classes, `Email` and `EmailWalker`.  The first class reads and parses an email into an easy to use object and the second class iterates through and creates an `Email` object for each email file in the directory.

**`Email`**

* `__init__(self, file_path)`: pass in the path to an email file.
* Class Members
    * `path`: full path to the email file in the file system
    * `folder`: name of the folder the email is in (e.g., inbox, _sent)
    * `frame`: name of the email file in the file system
    * `sender`: the email address of the sender
    * `recipients` a list containing all emails in the `to`, `cc`, and `bcc` fields
    * `to`: list of emails in `to` field
    * `cc`: list of emails in `cc` field
    * `bcc`: list of emails in `bcc` field
    * `subject`: subject line
    * `date`: `datetime` object of when the email was sent
    * `text`: the text content in the email
    
    

**`EmailWalker`**

* `__init__(self, email_root)`: pass in the root directory containing the email folders (e.g., inbox, _sent)
* `__iter__(self)`: returns an iterator that returns email objects

The `__iter__` method means that `EmailWalker` is an iterator, and can be conveniently used in a loop:

    walker = EmailWalker('./email_root')
    for email_object in walker:
        print email_object.subject




## TF-IDF

### Term Frequency (TF)

We would first like to get a sense of the terms (words) that describe the contents in each folder.  One way to do this is to count the number of times each term occurs in all of the emails in a folder.  The term that comes up the most must be best represent the folder!

    import os, sys, math
    sys.path.append('./util')
    from email_util import *
    from collections import Counter, defaultdict

    folder_tf = defaultdict(Counter)
    
    for e in EmailWalker(sys.argv[1]):
        words_in_email = e.text.split() # split the email text using whitespaces
        folder_tf[e.folder].update(words_in_email)
    
    for folder, counter in folder_tf.items():
        print folder
        for pair in sorted(counter.items(), key=lambda (k,v): v, reverse=True)[:20]:
            print '\t', pair    

But if we take a look at the output, they are non-descriptive words that are simply used often.  There are also random characters like `>`, which are clearly not words, but happen to pop-up often.

    sent
    	('the', 2529)
    	('to', 2041)
    	('and', 1357)
    	('of', 1203)
    	('in', 905)
    	('a', 883)
    	('>', 834)

This suggests that we need a better approach than term frequency, and that we need to clean the email text a bit.  We will walk you through how to do then in that order.

### Term Frequency - Inverse Document Frequency ([TF-IDF](http://en.wikipedia.org/wiki/Tf%E2%80%93idf))

Instead of the most popular terms, what we want popular items above background noise.  For example, "the" would be considered background noise because it is found multiple times in nearly every single email, so it is not very descriptive.  Similarly, "enron" is probably not very descriptive because we would expect most emails to mention the term.  

TF-IDF is a widely used metric that captures this idea by combining two intuitions.  The first intuition is Term Frequency, and the second is Inverse Document Frequency:

1. we want to increase a term's weight if it occurs often in a folder
1. we want to decrease a term's weight if it's also found in the other folders.

A term's IDF value is formally computed as 

    log( total # documents / # documents that contain term )

In our case, the numerator is the total number of emails and the denominator is the number of emails containing the term.  Finally, the TF-IDF is simply a multiple of the two values:

    TF * IDF

The following code will construct a dictionary that maps a term to its IDF value:


    allterms = Counter()
    nemails = 0
    for e in EmailWalker(sys.argv[1]):
        words_in_email = e.text.split() # split the email text using whitespaces
        unique_words_in_email = set(words_in_email)
        allterms.update(unique_words_in_email)
        nemails += 1
    
    idfs = {}
    for term, count in allterms.iteritems():
        idfs[term] = math.log( nemails / (1 + allterms[term]) )

If we combine `idfs` with each folder's `tf` value, we would compute the `tf-idf`.  If we print the top values for each folder, we would see something like:
    
    inbox
    	('>', 10022.526185338656)
    	('i', 3117.082870978074)
    	('=', 2287.3107850070046)
    	('<td', 1898.8767820921892)
    	('my', 1831.540344350006)
    	('our', 1706.1448843015744)
    	('will', 1703.0626226357856)
    	('it', 1691.8629245488892)
    	('have', 1689.8928262051465)
    	('was', 1660.9399256319914)

As we can see, the results are still not satisfying because there is still a lot of noise, and non-word characters pop up a lot.

### Cleaning The Data

The email dataset is a simple dump, and each file contains the email headers, attachments, and the actual message -- all of it is ascii-encoded.  In order to see sensible terms, we need to clean the data a bit.  This process varies depending on what your application is.  In our case, we want

* Reasonable english words.  These should only contain a-z characters (this is a simplification).
* We don't care about casing.  We want "enron" and "Enron" to be the same term.
* We don't care about really short words.  We want words with 4 or more characters. 

To do this, we will replace the code

    words_in_email = e.text.split() # split the email text using whitespaces

With a function that lowercases and filters all of the words in the email message

    import re
    refs_pat = '(?P<ref>[a-z]+)'
    refs_prog = re.compile(refs_pat)
    
    
    def get_terms(s):
        s = s.lower()
        arr = s.split()
        terms = []
        for term in arr:
            res = refs_prog.match(term)
            if res:
                val = res.group('ref')
                terms.append(val)
            else:
                terms.append('')
        
        terms = filter(lambda term: len(term) > 3, terms)
        return terms

    words_in_email = get_terms(e.text)

    




If we print the top TF-IDF terms in a folder, it should give a us a sense of the "important" terms.

We will explain TF-IDF is through a working example. HIGH LEVEL GOAL

family
	('pate', 28.456862272897595)
	('zach', 27.758052561021806)
	('beau', 26.63165691650491)
	('birth', 22.03620359114226)
	('july', 20.12631560920885)
	('gif', 19.469640452391875)
	('herrold', 17.69769940436878)
	('vermeil', 15.664106476001354)
	('photos', 15.482232610552046)
	('baby', 15.228560446467856)
all_documents
	('2000', 673.198316187371)
	('communications', 623.1569106172456)
	('subject', 577.0190473957614)
	('meeting', 561.5372620634564)
	('october', 550.5727152457546)
	('information', 542.6507085797787)
	('business', 535.4676171379596)
	('kenneth', 535.0885237924068)
	('call', 526.0046317653436)
	('also', 524.9851818411871)
compaq
	('rohde', 12.979760301594583)
	('lisa', 12.431429837590521)
	('org', 12.244310741343948)
	('chart', 10.709800435916613)
	('cap', 9.51055819081837)
	('org0301assts', 7.5884924394654005)
	('281-514-1297', 7.5884924394654005)
	('ceosec', 7.5884924394654005)
	('281-518-9882', 6.895345258905455)
	('admins', 6.741194579078197)
business
	('obligations', 16.65483153661308)
	('determine', 15.734058148108584)
	('commitments', 14.20758302865625)
	('imi', 12.979760301594583)
	('gathered', 12.244310741343948)
	('italian', 12.096094797036503)
	('proper', 11.593465940474692)
	('contractual', 11.285164580820176)
	('accordingly', 10.152373630978571)
	('purchasing', 10.047086164007728)
discussion_threads
	('2000', 513.613905215451)
	('october', 501.0503017051312)
	('compaq', 472.74602940188873)
	('transactions', 469.6840243058487)
	('business', 451.98526422983673)
	('today', 441.2075620981817)
	('attached', 432.22711668299377)
	('information', 404.161725660981)
	('day', 404.156450142581)
	('also', 402.61101357983813)
notes_inbox
	('october', 501.0503017051312)
	('2000', 474.8798248824608)
	('transactions', 467.58722062591187)
	('compaq', 461.9609488832144)
	('business', 432.5903741602728)
	('today', 430.09801916765196)
	('http', 404.32941903449694)
	('information', 401.33541988712796)
	('total', 400.92399694102124)
	('services', 393.7028955547116)
sec_panel
	('sec', 19.760863090686893)
	('panel', 19.67959774004035)
	('outline', 13.584664934321516)
	('blackstone', 13.482389158156394)
	('paper', 12.893091692431602)
	('agenda', 11.637809619643416)
	('sending', 11.172780293620809)
	('kindly', 9.99645054803915)
	('koller', 9.590568860045767)
	('discussion', 8.583313862259182)
enron
	('theme', 23.308765186991806)
	('downtown', 20.56196874815064)
	('comets', 16.173803586387542)
	('basketball', 15.395269999932289)
	('houston', 14.104388677691238)
	('cnpc', 13.79069051781091)
	('hamil', 13.79069051781091)
	('peters', 13.482389158156394)
	('gilman', 12.76903927027893)
	('reinvention', 12.76903927027893)
inbox
	('width', 1124.7760959321336)
	('2001', 973.7489633284944)
	('2002', 908.0217195724758)
	('know', 806.3892504784861)
	('height', 770.9997052301258)
	('message', 728.2842234603417)
	('src', 697.2557096425406)
	('center', 696.4062851600497)
	('management', 695.8930116655829)
	('people', 692.875362527725)
_sent
	('communications', 400.10298287952907)
	('rosalee', 370.0703109972345)
	('kenneth', 359.6738286648685)
	('subject', 294.71402958385664)
	('2001', 222.0237798330016)
	('meeting', 217.4968268555641)
	('april', 208.1267385328085)
	('klay', 201.74192070377475)
	('rosie', 200.0461406416558)
	('attend', 197.6654403467343)
calendar
	('casual', 11.192124549550389)
	('shoot', 10.709800435916613)
	('fortune', 9.056443289547678)
	('juanher', 8.68710472813351)
	('grooming', 8.68710472813351)
	('prhopkin', 8.68710472813351)
	('koeing', 8.68710472813351)
	('invitational', 8.68710472813351)
	('imceanotes-courtenay', 8.68710472813351)
	('plonzano', 8.68710472813351)
deleted_items
	('declared', 2167.2414912385375)
	('donate', 2151.410381760344)
	('bankruptcy', 2122.8656517030927)
	('millions', 2112.1347022777477)
	('bills', 2109.5925729588625)
	('retirement', 2089.979970603285)
	("company's", 2054.731495227359)
	('funds', 2022.7363807665545)
	('pay', 1919.2160604817207)
	('underhanded', 1865.9432555056947)
sent_items
	('image', 91.7845084332862)
	('associate', 30.136990418443084)
	('atroche851088951', 29.20324146805448)
	('program', 26.652913385413708)
	('mccann', 24.808792313382042)
	('loy', 22.7654773183962)
	('original', 22.17854411337738)
	('wired', 21.90243110104086)
	('rotating', 21.90243110104086)
	('continue', 20.784478821493316)
sent
	('communications', 400.10298287952907)
	('rosalee', 371.9877737485155)
	('kenneth', 364.09604786976445)
	('subject', 296.78219821251525)
	('2001', 222.0237798330016)
	('meeting', 218.48544879581667)
	('april', 208.1267385328085)
	('klay', 201.74192070377475)
	('rosie', 200.0461406416558)
	('attend', 199.8864003506302)
elizabeth
	('wedding', 76.45664976382045)
	('love', 48.94235804860213)
	('liz', 47.65461399153731)
	('dad', 42.015273054457204)
	('jose', 41.87295057803246)
	('band', 39.498076032870614)
	('elizabeth', 38.90630505950411)
	('lora', 38.27760232285716)
	('linda', 38.09341184613746)
	('yahoo', 37.108720182380054)


## N-grams



## Cosine Similarity



## Done!



## Notes

Email dataset

* Email script to download gmail email messages without attachments
* Download the folders
* Extract the data into files.  
* 1 file per email


TF-IDF

Enron dataset
* Kenneth Lay (lay-k)
* Jeffery Skilling
* `lay-k/ skilling-j/ whalley-g/ pereira-s/ `
