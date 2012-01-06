# Day 4: Text Processing

## Overview

Today we will discuss text processing.  Our exercises will be grounded in an email dataset (either yours or Kenneth Lay's).  After today, you will be able to compute the most important terms in a particular email, find emails similar to the one you are reading, and find people that tend to send you similar emails.

As opposed to the data we've seen so far, we will need to clean the data before we can extract meaningful results.

The techniques will include

* [Tf-Idf](http://en.wikipedia.org/wiki/Tfidf)
* [Regular Expressions](http://en.wikipedia.org/wiki/Regular_expression) and data cleaning
* [N-gram](http://en.wikipedia.org/wiki/N-gram)
* [Cosine Similarity](http://en.wikipedia.org/wiki/Cosine_similarity)


## Setting Up

### Dataset


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




## Folder Summaries

In this section, we will automatically extract key terms that describe the emails in a folder.  This is useful for two purposes.  First, it can be a crude summary of the emails in each folder.  Second, it is used to search for and retrieve emails.  For example, if a term (e.g., "lawsuit") is representative of an email, then we would like to retrieve that email when we search for "lawsuit".  

Today, we will focus on the first purpose.

### Term Frequency (TF)

One way to do this is to count the number of times each term occurs in all of the emails in a folder.  The term that comes up the most must be best represent the folder!

    import os, sys, math
    sys.path.append('./util')
    from email_util import *
    from collections import Counter, defaultdict

    folder_tf = defaultdict(Counter)
    
    for e in EmailWalker(sys.argv[1]):
        terms_in_email = e.text.split() # split the email text using whitespaces
        folder_tf[e.folder].update(terms_in_email)
    
    for folder, counter in folder_tf.items():
        print folder
        for pair in sorted(counter.items(), key=lambda (k,v): v, reverse=True)[:20]:
            print '\t', pair    

But if we take a look at the output, they are non-descriptive terms that are simply used often.  There are also random characters like `>`, which are clearly not words, but happen to pop-up often.

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

The following code will construct a dictionary that maps a term to its IDF value.  Fill in the last part to calculate the tf-idf.


    allterms = Counter()
    nemails = 0
    for e in EmailWalker(sys.argv[1]):
        terms_in_email = e.text.split() # split the email text using whitespaces
        unique_terms_in_email = set(terms_in_email)
        allterms.update(unique_terms_in_email)
        nemails += 1
    
    idfs = {}
    for term, count in allterms.iteritems():
        idfs[term] = math.log( nemails / (1 + allterms[term]) )


    tfidfs = {} # key is folder name, value is a list of (term, tfidf score) pairs
    for folder, tfs in folder.iteritems:
        #
        # write code to calculate tf-idfs yourself!
        # 
        pass

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

As we can see, there is a lot of noise, and non-word characters pop up a lot.  We will deal with this next.

In addition, there are a number of extensions

### Regular Expressions and Data Cleaning

The email dataset is a simple dump, and each file contains the email headers, attachments, and the actual message -- all of it is ascii-encoded.  In order to see sensible terms, we need to clean the data a bit.  This process varies depending on what your application is.  In our case, we decided that we want

1. We don't care about casing.  We want "enron" and "Enron" to be the same term.
1. We don't care about really short words.  We want words with 4 or more characters. 
1. We don't care about [stop words](http://en.wikipedia.org/wiki/Stop_words).  We pre-decided that words like "the" and "and" should be ignored.
1. Reasonable words.  These should only contain a-z characters, hyphens, and apostrophes.  It should also start and end with an a-z character.

Let's tackle each of these requirements one by one!

#### 1-2. Casing and Short Words

We can deal with these by lower casing all of the terms and filtering out the short terms.

    terms = e.text.lower().split()
    terms = filter(lambda term: len(term) <= 3, terms)

#### 3. Stop Words

The `email_util` module defines a variable `STOPWORDS` that contains a list of common english stop words in lower case.  We can filter out terms that are found in in this list.

    from email_util import STOPWORDS
    terms = filter(lambda term: term in STOPWORDS, terms)
    


#### 4. Reasonable Words (Regular Expressions)

The last requirement is more difficult to enforce.  One way is to iterate through the characters in every term, and make sure they are valid:

    arr = e.text.split()
    terms = []
    for term in arr:
        valid = True
        for idx, c in  enumerate(term.lower()):
            if (idx == 0 or idx == len(term)-1):
                if (c < 'a' or c > 'z'):
                    valid = False
                    break
            elif (c != "'" and c != "-" and (c < 'a' or c > 'z')):
                valid = False
                break
        if valid:
            terms.append(term)

This is a pain in the butt to write, and is hard to understand and change.  All we are doing is making sure each term adheres to a pattern.  Regular Expressions (regex) is a very convenient language for finding and extracting patterns in text.  We don't have time for a complete tutorial, but we will talk about the basics.

Regex lets you specify:

* Classes of characters.  You may only care about upper case characters, or only digits and hyphens.  
* Repetition.  You can specify how many times a character or pattern should be repeated.
* Location of the pattern.  You can specify that the pattern should be at the beginning of the term, or the end.

It's easiest to show examples, so here's code that defines a pattern of strings that start with either `e` or `E`, followed the characters `nron`.  `re.search` checks if the pattern is found in `term` and returns `None` if the pattern was not found.

    import re
    term = "enronbankrupt"
    pattern = "[eE]nron+"
    if re.search(pattern, term):
        print "found!"    

The most basic pattern is a list of characters.  `pattern = "enron"` looks for the exact string `"enron"` (lower case).  But what if we want to match `"Enron"` and `"enron"`?  That's where character classes come in!

Brackets `[]` are used to define a character class.  That means any character in the class would be matched.  You simply list the characters that are in the class.  For example `[eE]` matches both `e` and `E`.  Thus `[eE]nron` would match both `"Enron"` and `"enron"`.  `[0123456789\-]` means that all digits and hyphens should be matched.  We need to escape `-` within `[]` because it is a special character.

It's tedious to list individual characters, so `-` can be used to specify a range of characters.  `[a-z]` is all characters between lower case `a` and `z`.  `[A-Z]` are all upper case characters.  `[a-zA-Z]` are all upper or lower case characters.  There are other shortcuts for common classes.  For example, `\w` is shorthand for `[a-zA-Z0-9]`

`[a-z]` only matches a single character.  We can add a special character at the end of the class to specify how many times it should be repeated:

* `?`: 0 or 1 times.  For optional characters
* `*`: 0 or more times.
* `+`: 1 or more times
* `{n}`: exactly `n` times
* `{n,m}`: between `n` and `m` times (inclusive).

For example, `[0-9]{3}-[0-9]{3}-[0-9]{4}` matches phone numbers that contain area codes.  Note that we didn't escape the `-` because it specifies a range within `[]` and is not interpreted as a range outside the `[]`.  This pattern fails if the user inputs `(510)-232-2323` because it doesn't recognize the `()`.  Can you modify the pattern to optionally allow `()`?

Finally, `^` and `$` are special characters for the beginning and the end of the text, respectively.  For example `^enron` means that `"enron"` must be at the beginning of the string.  `enron$` means that the `"enron"` should be at the end.  `^enron$` means the term should be exactly `"enron"`.


Great!  You should know enough to create a pattern to find "reasonable words", and use it to re-compute the `tfidfs` dictionary and print the 10 most highly scored terms in each folder!




## [Cosine Similarity](http://en.wikipedia.org/wiki/Cosine_similarity)

It would be helpful to find email senders that send similar emails to Kenneth Lay.  That way, if we are reading an interesting email about Enron's bankruptcy, we can find other people that have sent similar emails.  [Cosine similarity](http://en.wikipedia.org/wiki/Cosine_similarity) is a common tool to achieve this.

The main idea is that emails that share terms with high tf-idf values are probably similar.  Also, they are more similar if they share more terms.  


Let's say we have a total of 1000 terms across all of the email senders.  Every email sender has a tf-idf score for each of the 1000 terms.  We could model all of the scores as a 1000-dimensional vector, where each dimension corresponds to a term, and the distance along the dimension is the term's tf-idf value.  The cosine of the two email senders' vectors measures the similarity between them.  Suppose the vectors were A and B.  Then the cosine would be:

    cos(A,B) = (A·B) / ((|A| * |B|) + 1)

The numerator is the sum of all the tfidf terms the senders have in common.  The denominator is the product of the vector lengths.  We typically add `1` in case the vectors are both 0.

A `cos(A,B)` of 1 means they are identical and 0 means the senders are independent from each other (the vectors are orthogonal).  

Here is how we would calculate the cosine similarity of two _folders_, using the `tfidfs` dictionary you computed in the previous section.  We assume that each value in `tfidfs` is a list of `(term, tfidf-score)` pairs
    
    from math import *
    sec_scores = dict(tfidfs['sec_panel'])
    fam_scores = dict(tfidfs['family'])

    # loop through terms in sec_scores
    # if term also exists in fam_scores, multiply both tfidf values and 
    # add to numerator
    numerator = 0.0
    for sec_key, sec_score in sec_scores.iteritems():
        dotscore = sec_score * fam_scores.get(sec_key, 0.0)
        numerator += dotscore
    
    # compute the l2 norm of each vector
    denominator = 0.0
    sec_norm = sum( [score**2 for score in sec_scores.values()] )
    sec_norm = math.sqrt(sec_norm)
    fam_norm = sum( [score**2 for score in fam_scores.values()] )
    fam_norm = math.sqrt(fam_norm)
    denominator = sec_norm * fam_norm + 1.0

    similarity = numerator / denominator

    
Now, modify the code you have written so far to compute the cosine similarity between every pair of folders.  Which folders are most similar?

## N-grams

Finally, only one word per term.  Not really clear.  "expensive", even though one could be part of the phrase "not expensive" whereas the other is "very expensive".  One popular way to add more context is to simply use more than one word per term (notice that we've used the word "term" instead of word for this reason).

# Exercise 1: Similar Email Senders

We computed the tf-idf and cosine similarity between every folder in kenneth's emails.  Now do the same, but for email senders.

# Exercise 2: Analyze Your Emails

We have written a script (`dataiap/resources/download_emails.py`) that you can use to download your own email over IMAP.  However before you can run it, you will need to install the following python modules:

- [dateutil](http://labix.org/python-dateutil#head-2f49784d6b27bae60cde1cff6a535663cf87497b)
    * PIP users can type `sudo pip install python-dateutil`
- [pyparsing](http://pyparsing.wikispaces.com/Download+and+Installation)
    * PIP users can type `sudo pip install pyparsing`

You can now run the script using the following command:

    python download_emails.py [IMAP ADDRESS]

You can pass the optional imap address parameter, otherwise it will default to gmail's imap address.  The script will then ask you to input your email and password, then create the folder `./[YOUR EMAIL]/` and download your email folders into that directory.  If you have a lot of emails, it can take a long time. 

See if you can uncover something interesting!

## Done!

### What Else Can We Do?


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
