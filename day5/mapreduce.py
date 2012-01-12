"""
export AWS_ACCESS_KEY_ID='my_key_id'
export AWS_SECRET_ACCESS_KEY='my_access_id'

python -m mrjob.tools.emr.create_job_flow --num-ec2-instances=5
python -m mrjob.tools.emr.terminate_job_flow.py JOBFLOWID
python -m mrjob.tools.emr.audit_usage
python mr_my_job.py -r emr --emr-job-flow-id=JOBFLOWID input_file.txt > out
python mr_my_job.py -r emr --emr-job-flow-id=j-JOBFLOWID -o 's3://test_enron_json_123/output' --no-output 's3://test_enron_json_123/*.json'
python simple_wordcount.py < lay-k.json
python mr_wordcount.py < lay-k.json
"""
"""
In day 4, we saw how to process text data using the Enron email dataset.  In reality, we only processed a small fraction of the entire dataset: about 20 megabytes of Kenneth Lay's emails.  The entire dataset is $$$ gigabytes, a factor of $$$ larger than what we worked with.  And what if we worked on GMail, Yahoo! Mail, or Hotmail?  We'd have several petabytes worth of emails, a factor of at least $$$ the size of the data we dealt with.

All that data would take a while to process, and it certainly couldn't fit on or be crunched by a single laptop.  We'd have to store the data on many machines, and we'd have to process it (tokenize it, calculate tf-idf) using multiple machines.  There are many ways to do this, but one of the more popular recent methods of _parallelizing data computation_ is on a programming framework called MapReduce, an idea that [Google presented to the world in $$$]($$$).  Luckily, you do not have to work at Google to benefit from MapReduce: an open-source implementation called [Hadoop]($$$) is available for your use!

But we don't have hundreds of machines sitting around for us to use them, you might say.  Actually, we do!  [Amazon Web Services]($$$) offers a service called Elastic Mapreduce$$$ (EMR) that gives us access to as many machines as we would like for about $$$ cents per hour of machine we use.  Use $$$ machines for $$$ hours?  Pay Amazon $$$.  If you've ever heard the buzzword *cloud computing*, this elastic service is part of the hype.

Let's start with a simple word count example, then rewrite it in MapReduce, then add TF-IDF calculation, and finally, run it on $$$ machines on Amazon's EMR!
<h3>Setup</h3>
Copy the python and tar files to wherever your code is$$$.

<h3>Counting Words</h3>

We're going to start with a simple example that should be familiar to you from day 4's lecture.  First, unzip the JSON-encoded Kenneth Lay email file:
"""

unzip dataiap/datasets/emails$$$

"""

This will result in a new file called $$$, which is JSON-encoded.  What is JSON?  You can think of it like a text representation of python dictionaries and lists.  If you open up the file, you will see on each line something that looks like this:

$$$

It's a dictionary representing an email sent to or received by Kenneth Lay.  It contains the same content that we dealt with yesterday, but encoded into JSON, and rather than one file per email, we have a single file with one email per line.

Why did we do this?  Big data crunching systems like Hadoop don't deal well with lots of small files: they want to be able to send a large chunk of data to a machine and have to crunch on it for a while.  So we've processed the data to be in this format: one big file, a bunch of emails one per line.  If you're curious how we did this, check out $$$.

Aside from that, processing the emails is pretty similar to what we did on day 4.  Let's look at a script that counts the words in the text of each email (As an aside: it would help if you wrote and ran your code in `dataiap/day5/...` today, since several modules like `term_tools.py` are available in that directory).

"""

import sys
from collections import defaultdict
from mrjob.protocol import JSONValueProtocol
from term_tools import get_terms

input = open(sys.argv[1])
words = defaultdict(lambda: 0)
for line in input:
    email = JSONValueProtocol.read(line)[1]
    for term in get_terms(email['text']):
        words[term] += 1

for word, count in words.items():
    print word, count

"""

You can save this script to `exercise1.py` and then run `python exercise2.py path/to/lay-k.json`.  It will print the word count in due time.  `get_terms` is similar to the word tokenizer we saw on day 4.  `words` keeps track of the number of times we've seen each word.  `email = JSONValueProtocol.read(line)[1]` uses a JSON decoder to convert each line into a dictionary called email, that we can then tokenize into individual terms.

As we said before, running this process on several petabytes of data is infeasible because a single machine might not have petabytes of storage, and we would want to enlist multiple computers in the counting process to save time.

We need a way to tell the system how to divide the input data amongst multiple machines, and then combine all of their work into a single count per term.  That's where MapReduce comes in!

<h3>MapReduce</h3>
MapReduce is named after its two most important bits of functionality: *map* and *reduce*.  Let's explain this with an example.  Say we have a JSON-encoded file with emails (1,000,000 emails on 1,000,000 lines), and we have 10 machines to process it.

In the *map* phase, we are going to send each machine 100,000 lines, and have them break each of those emails into the words that make them up:

$$$

Once each machine has tokenized all of the words in the email, they will *shuffle* each word to a machine pre-designated for that word (using a hash function$$$, if you're curious).  This part is automatic, but it's important to know what's happening here:

$$$

And finally, once each machine has received the words that its responsible for, the *reduce* phase will turn all of the occurrences of words it has received into counts of those words:

$$$

MapReduce is more general-purpose than just serving to count words.  Some people have used it to do exotic things like [process millions of songs]($$$), but we'll stick to the boring stuff.

Without further ado, here's the wordcount example, but in MapReduce

"""

import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield term, 1

    def reducer(self, term, occurrences):
        yield None, {'term': term, 'count': sum(occurrences)}

if __name__ == '__main__':
        MRWordCount.run()

"""

Too cool!  Let's break this thing down.  You'll notice the terms MRJob in a bunch of places.  [MRJob]($$$) is a python package that makes writing MapReduce programs easy.  To create a MapReduce program, you have to create a class (like `MRWordCount`) that has a `mapper` and `reducer` function.  If the program is run from the command line, (the `if __name__ == '__main__':` part) we run the MRWordCount MapRedce program.

Looking inside `MRWordCount`, we see `INPUT_PROTOCOL` being set to `JSONValueProtocol`.  By default, map functions expect a line of text as input, but we've encoded our emails as JSON, so we let MRJob know that.  Similarly, we explain that our reduce tasks will emit dictionaries, and set `OUTPUT_PROTOCOL` appropriately.

The `mapper` function handles the functionality described in the first image of the last section.  It takes each email, tokenizes it into terms, and `yield`s each term.  You can `yield` a key and a value (`term` and `1`) in a mapper.  We yield the term with the value `1`, meaning one instance of the word `term` was found.

The `reducer` function implements the third image of the last section.  We are given a word (the key emitted from mappers), and a list `occurrences` of all of the values emitted for each instance of `term`.  Since we are counting occurrences of words, we emit a dictionary containing the term and a sum of the occurrences we've seen.

Note that we `sum` instead of `len` the `occurrences`.  This allows us to change the mapper implementation to emit the number of times each word occurs in a document, rather than `1` for each word.

Both the `mapper` and `reducer` offer us the parallelism we wanted.  There is no loop through our entire set of emails, so MapReduce is free to distribute the emails to multiple machines, each of which will run `mapper` on an email-by-email basis.  We don't have a single dictionary with the count of every word, but instead have a `reduce` function that has to sum up the occurrences of a single word, meaning we can again distribute the work to several reducing machines.

<h3>Run It!</h3>
Enough talk!  Let's run this thing.

"""

$$$ (parallel input/output style to the EMR version if you can)

"""

That's going to do something similar to what the simple wordcount script did.  The only difference you will notice is that the output comes out in dictionaries (`OUTPUT_PROTOCOL = JSONValueProtocol`), and in sorted term order (that's how all of the occurrences for a term end up on a single reducer).

If we want to write the output to disk, we can instead write
"""

$$$

"""
If you re-run the program, it take a look at $$$ for the output.

You will notice we have not yet run tasks on large datasets (we're still using `lay-k.json`) and we are still running them locally on our computers.  We will learn a few things before we move onto Amazon's machines, but this is an important lesson still: MapReduce tasks will take a long time to run and hold up several tens to several hundreds of machines.  Test them locally like we just did to make sure you don't have bugs before going to the full dataset.

<h3>Show off What you Learned</h3>
"""

"""
** Exercise **  Create a second version of the MapReduce wordcounter that counts the number of each word emitted by each sender.  You will need this for later, since we're going to be calculating TF-IDFimplementing  terms per sender.  You can accomplish this with a sneaky change to the `term` emitted by the `mapper`.  You can either turn that term into a dictionary, or into a more complicated string, but either way you will have to encode both sender and term information in that `term`.
"""

"""
** Bonus Exercise ** Grep.  The [`grep` command]($$$) on UNIX-like systems allows you to search text files for some term or terms.  Typing `grep hotdogs file1` will return all instances of the word `hotdogs` in the file `file1`.  Implement a `grep` for emails.  When a user uses your mapreduce program to find a word in the email collection, they will be given a list of the subjects and senders of all emails that contain the word.  You might find you do not need a particularly smart reducer in this case: that's fine.  If you're pressed for time, you can skip this exercise.
"""

"""
<h3>TF-IDF</h3>
On [day 4](./day4/), we learned that counting words is not enough to summarize text: common words like `the` and `and` are too popular.  In order to discount those words, we multiplied by the term frequency of `wordX` by `log(total # documents/# documents with wordX)`.  Let's do that with MapReduce!

We're going to emit a per-sender TF-IDF.  To do this, we need three MapReduce tasks:

* The first will calculate the number of documents, for the numerator in IDF.

* The second will calculate the number of documents each term appears in, for the denominator of IDF, and emits the IDF (`log(total # documents/# documents with wordX)`).

* The third calculates a per-sender IDF for each term after taking both the second MapReduce's term IDF and the email corpus as input.

<h3>MapReduce 1: Total Number of Documents</h3>

Eugene and I are the laziest of instructors.  We don't like doing work where we don't have to.  If you'd like a mental exercise as to how to write this MapReduce, you can do so yourself, but it's simpler than the wordcount example.  Our dataset is not so large that we can't just use the `wc` UNIX command to count the number of lines in our corpus:
"""

wc -l lay-k.json

"""

Kenneth Lay has 5929 emails in his dataset.  We ran wc -l on the entire Enron email dataset, and got 516893.  This took a few seconds.  Sometimes, it's not worth overengineering a simple task!:)

<h3>MapReduce 2: Per-Term IDF</h3>
We recommend you stick to 516893 as your total number of documents, since eventually we're going to be crunching the entire dataset!

What we want to do here is emit `log(516893.0 / # documents with wordX)` for each `wordX` in our dataset.  Notice the decimal on 516893**.0**: that's so we do [floating point division]($$$) rather than integer division.  The output should be a file where each line contains `{'word': 'wordX', 'idf': 35.92}` for actual values of `wordX` and `35.92`.

We've put our answer in `per-term-idf.py` $$$, but try your hand at writing it yourself before you look at ours.  It can be implemented with a two-line change to the original wordcount MapReduce we wrote.

<h3>MapReduce 3: Per-Sender TF-IDFs</h3>

The third MapReduce multiplies per-sender term frequencies by per-term IDFs.  This means it needs to take as input the IDFs calculated in the last step ** as well as ** calculate the per-sender TFs.  That requires something we haven't seen yet: initialization logic.  Let's show you the code, then tell you how it's done.

"""

$$$

"""

If you did the [first exercise ](#firstexercise###), the `mapper` and `reducer` functions should look a lot like the per-sender word count `mapper` and `reducer` functions you wrote for that.  The only difference is that `reducer` takes the term frequencies and multiplies them by `idf[word]`, to normalize by each word's IDF.

`idf` is a dictionary that is loaded onto each reducer before it begins its work.  The $$$....

We now now how to write some pretty gnarly MapReduce programs, but they all run on our laptops.  Sort of boring.  It's time to move to the world of distributed computing, Amazon-style!

<h3>Amazon Web Services</h3>
[Amazon Web Services]($$$) (AWS) is Amazon's gift to people who don't own datacenters.  It allows you to elastically request computation and storage resources at varied scales using different services.  As a testiment to the flexibility of the services, companies like NetFlix are moving their entire operation into AWS.

There are more than a day's worth of AWS services to discuss, so let's stick with two of them: Simple Storage Service (S3) and Elastic MapReduce (EMR).

<h3>AWS S3</h3>
S3 allows you to store gigabytes, terabytes, and, if you'd like, petabytes of data in Amazon's datacenters.  This is useful, because laptops often don't crunch and store more than a few hundred gigabytes worth of data, and storing it in the datacenter allows you to securely have access to the data in case of hardware failures.  It's also nice because Amazon tries harder than you to have the data be always accessible.

In exchange for nice guarantees about scale and accessibility of data, Amazon charges you rent on the order of $$$ per gigabyte stored per month.

Services that work on AWS, like EMR, read data from and store data to S3.  When we run our MapReduce programs on EMR, we're going to read the email data from S3, and write word count data to S3.

S3 data is stored in ** buckets **.  Within a bucket you create, you can store as many files or folders as you'd like.  The name of your bucket has to be unique across all of the people that store their stuff in S3.  Want to make your own bucket?  Let's do this!

"""



