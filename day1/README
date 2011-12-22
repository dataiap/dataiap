# DataIAP Day 1 Materials

# Introduction 

## Prereqs

We assume you have a working knowledge of python (6.01) and are willing to write code.

## What we will teach

We will teach the basics of data analysis through concrete examples.
You will be expected to   All of your programming will be
written in python.  Practice using common statistical analysis tools.  Generating common plots.

## What we will not teach

* *R*.  We will use functions in R, and provide wrappers so that you do
 not need to program in it.  Learning R is enough material for a separate course.
* Visualization using browser technology (canvas, svg, d3, etc) or in
  non python languages ([Processing](http://processing.org/).  These
  tools are very interesting, and lots of visualizations on the web use
  these tools (e.g., [nytimes
  visualizations](http://open.blogs.nytimes.com/2008/10/27/the-new-york-times-data-visualization-lab/)),
  however they are out of the scope of this class.  SAY WHY OK
* Fancy, interactive visualizations.  

## Programming Environment

We assume that you are developing in a unix-like environment and are familiar with the common commands.  If you are a windows user, we assume you are using cygwin.  

## Tools and Libraries 

In this class, you will need to install a number of tools.  The major
ones are:

* [python 2.7](http://www.python.org/getit/releases/2.7/)
	* Python is
  usually installed in Mac OSX and major unix distributions.  Type
  `python --version` to make sure it is the right version
* [R](http://software.rc.fas.harvard.edu/mirrors/R/)
	* R is widely used
  for statistical computing, and we will use it in day 3 to analyze
  our datasets.  We will not program directly in R, rather, we have
  written wrappers for the functions that will be used.
* [easy_install](http://pypi.python.org/pypi/setuptools#files)
	* python package manager.
* [pip](http://pypi.python.org/pypi/pip#downloads).  
	* Makes installing python packages really really easy.  Requires easy_install

We will also require a number of python modules:

- [numpy 1.6.x](http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/)
	* PIP users can type `sudo pip install numpy`
- [scipy 0.10](http://sourceforge.net/projects/scipy/files/scipy/0.10.0/)
	* Unfortunately, we were unable to install scipy using PIP, so you will likely need to compile it from source.
    * Ubuntu users can type `sudo apt-get install python-scipy`
- [matplotlib 1.1.0](http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.0/)
    * PIP users can type `sudo pip install matplotlib`
    * Note: If compiling from source, matplot lib requires a number of other libraries: 
    ([libpng](http://www.libpng.org/pub/png/libpng.html), [freetype 2](http://download.savannah.gnu.org/releases/freetype/))
- [mrjob](https://github.com/yelp/mrjob)
	* MapReduce package.  We will use it in day 5.
	* PIP users can type `sudo pip install mrjob`
	* If compiling from source, it requires [boto](http://code.google.com/p/boto/downloads/list)


## Datasets

We will be working with several datasets in this course.  Some are fairly large, so we ask that you download them before the class, and place them in 

* [2008 Presidential Campaign Donations](http://fec.gov/disclosurep/PDownload.do): click "All.zip" and unzip the file
* 2011 County Health Rankings: This file should be in `dataiap/datasets/county_health_rankings/additional_measures_cleaned.csv`
* [Associated Press News Articles](http://web.mit.edu/~eugenewu/Public/blah): Before the class, we scraped several weeks of news articles from the AP's [rss feeds](http://hosted2.ap.org/APDEFAULT/APNewsFeeds).


# OK.  Let's play with some data!


Today we will play investigative reporter analyze the presidential campaign donations dataset. We will go through the full process of downloading a new dataset, the initial steps of understanding the data, visualizing it, coming up with hypotheses, and exploring the dataset.  Hopefully, you'll learn something new about presidential elections.

A lot of other organizations have analyzed the data:

* [FEC](http://fec.gov/disclosurep/pnational.do)
* [http://www.pitchinteractive.com/election2008/](http://www.pitchinteractive.com/election2008/)
* [http://www.pitchinteractive.com/election2008/jobarcs.html](http://www.pitchinteractive.com/election2008/jobarcs.html)

These visualizations are beautiful but high level overviews, which tend to hide interesting details.  We will uncover some of them today.  We provide the commands and code to initially explore the data, and ask you to further analyze the data in the exercises.

## First Steps

We assume that you have already [downloaded the dataset](http://fec.gov/disclosurep/PDownload.do).  We need to first unzip the file and rename it to something meaningful:

    > unzip P00000001-ALL.zip
    > mv P00000001-ALL.txt donations.txt

Lets see how much data we are dealing with.  The word count (`wc`) command will tell us the number of lines in this file:

	> wc -l donations.txt
	4938656

Let's take a quick look at the file.  `head` prints the first N lines in a file.  Line 1 looks like names of each field in the file, and the data starts from line 2.

	> head -n3 donations.txt	cmte_id,cand_id,cand_nm,contbr_nm,contbr_city,contbr_st,contbr_zip,contbr_employer,contbr_occupation,contb_receipt_amt,contb_receipt_dt,receipt_desc,memo_cd,memo_text,form_tp,file_num
    C00420224,"P80002983","Cox, John H","BROWN, CHARLENE","EAGLE RIVER","AK","99577","","STUDENT",25,01-MAR-07,"","","","SA17A",288757
    C00420224,"P80002983","Cox, John H","KELLY, RAY","HUNTSVILLE","AL","35801","ARKTECH","RETIRED",25,25-JAN-07,"","","","SA17A",288757

If we take a look at the [file format description](ftp://ftp.fec.gov/FEC/Presidential_Map/2012/DATA_DICTIONARIES/CONTRIBUTOR_FORMAT.txt) on the fec.gov website, it specifies that

	The text file is comma delimited and uses double-quotation marks as the text qualifier.

The file contains information about the candidate, the donor's city, state, zip code, employer and occupation information, as well as the amount donated.  In addition it contains the date of the donation, 

Let's write a script to read and print each donation's date, amount and candidate.  Python comes with a csv module that helps reads CSV (comma separated values) files.  DictReader assumes that the first line are the names of the fields, and creates a dictionary for each row of `fieldname->value` pairs.


	import csv,sys,datetime
	reader = csv.DictReader(open(sys.argv[1], 'r'))
	
	for row in reader:
	    name = row['cand_nm']
	    datestr = row['contb_receipt_dt']
	    amount = row['contb_receipt_amt']
	    print ','.join(map(str, [name, datestr, amount]))



### Introducing `matplotlib`

We will be using `matplotlib` in the rest of the course, and work with it extensively in day 2.  So the following will be a very simple crash course on how to graph a line:

	# pyplot is the plotting module
	import matplotlib.pyplot as plt
	import random
	
	# generate the data
	xs = range(10)
	ys1 = range(10)
	ys2 = [random.randint(0, 20) for i in range(10)]
	
	# create a 10 inch x 5 inch figure
	fig = plt.figure(figsize=(10,5))

	# draw a line graph
	plt.plot(xs, ys1, label='line 1')
	plt.plot(xs, ys2, label='line2')

	# create the legend
	plt.legend(loc='upper center', ncol = 4)

	# finally, render and store the figure in an image
	plt.savefig('/tmp/test.png', format='png')

`plt.plot()` takes a list of x and a list of y values, and draws a line between every pair of (x,y) points.  The line is drawn on the most recently created figure.  It is smart and understands date objects, ints, and floats, and takes care of scaling for us.

`plt.legend()` draws the legend in the figure.  There are a bunch of other common chart objects like x-axis labels that `matplotlib` supports.

### Sampling The Data

The dataset is quite large, and processing the full dataset can be pretty slow.  It is often useful to sample the dataset and try things out on the sample before doing a complete analysis of all of the data.  The following is a script that samples the donations dataset.  It will print 1 out of every 1000 donations (or roughly 5000 total donations):

	import sys
	
	with file(sys.argv[1], 'r') as f: 
		i = 0
		for line in f:
			if i % 1000 == 0:
				print line[:-1]
			i += 1

We will be analyzing Obama vs McCain data, so you can modify this code to create a file that only contains donations for McCain and Obama.  That way later analysis will run faster.
	


## Plotting The Data

We learned how to iterate and extract data from the dataset, and how to plot lines, so we will now combine the two  to plot Obama's campaign contributions by date.  We will compute the total amount of donations for each day, and use `matplotlib` to create the charts.

We parse the dates using the `datetime` module's `strptime` function.  ([Format codes](http://docs.python.org/library/datetime.html#strftime-strptime-behavior)).


	from collections import defaultdict
	import  matplotlib.pyplot as plt
	
	reader = csv.DictReader(open(sys.argv[1], 'r'))
	
	obamadonations = defaultdict(lambda:0)
	
	for row in reader:
	    name = row['cand_nm']
	    datestr = row['contb_receipt_dt']
	    amount = float(row['contb_receipt_amt'])
	    date = datetime.datetime.strptime(datestr, '%d-%b-%y')
	
	    if 'Obama' in name:
	        obamadonations[date] += amount
	
	
	# dictionaries 
	sorted_by_date = sorted(obamadonations.items(), key=lambda (key,val): key)
	xs,ys = zip(*sorted_by_date)
	plt.plot(xs, ys, label='line 1')
	plt.legend(loc='upper center', ncol = 4)
	plt.savefig('/tmp/test.png', format='png')

`defaultdict` is a convenience dictionary.  When we use a regular dictionary, it throws an error when we access a key that doesn't exist:

	>>> d = {}
	>>> d['foo']
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	KeyError: 'foo'

However, we provide `defaultdict` a function to call and return if the key doesn't exist.  This is nice because we can assume a default value.  It is otherwise used as a normal python dictionary. 
	
	>>> d = collections.defaultdict(lambda:0)
	>>> d['foo']
	0
	>>> d['bar'] += 1

In the loop that reads the data, we record the total donation amount for each date.  

Finally, we need to sort the data in `obamadonations` by the date (the key).  `sorted(l, key=f)` returns a sorted copy of `l` and calls `f` to extract the item to compare with.  `zip(*pairs)` then unzips the list of pairs.

You should see something like this:

<img src="./graph1.png" width="80%">

Great!  It's interesting to see a spike in donations on August 2008 -- does it relate to the amazing [democratic convention speech](http://elections.nytimes.com/2008/president/conventions/videos/20080828_OBAMA_SPEECH.html) he gave on August 28th?  At this point a reporter may try to understand some of the spikes in the graph.  

**But wait!** There's a really weird _dip_ in his donations in the lower right corner.  How does someone give negative donations?  The next part will investigate this further.

<!--Notice that the graph doesn't have any labels, and the y-axis is at an incomprehensible scale.  Don't worry about it for today, we'll go into details on customizing graphs tomorrow.-->


## The Case of the Negative Donation

The first thing we should do is look at some of the data where the donation amount is negative and see if there's anything interesting.  We can modify our existing code.  Note that we cast `amount` into a float.  The CSV module returns strings, so its our job to cast the data into the proper type.

	import csv,sys,datetime
	reader = csv.DictReader(open(sys.argv[1], 'r'))
	
	for row in reader:
	    name = row['cand_nm']
	    datestr = row['contb_receipt_dt']
	    amount = float(row['contb_receipt_amt'])
		if amount < 0:
			line = '\t'.join(row.values())
			print line

If you scan through the output, you'll see data such as:

	C00430470	DARIEN	RETIRED	McCain, John S	SA17A	P80002801	068202003		VAN MUNCHING, LEO MR. JR.	02-AUG-07	CT	X	REATTRIBUTION TO SPOUSE	315387	REATTRIBUTION TO SPOUSE	-2300
	
	C00430470	LOS ANGELES	EXECUTIVE	McCain, John S	SA17A	P80002801	900492125	A.E.G.	LEIWEKE, TIMOTHY J. MR.	30-APR-08	CA	X	REFUND; REDESIGNATION REQUESTED	364146	REFUND; REDESIGNATION REQUESTED	-2300

Lots of text, but "REDESIGNATION TO GENERAL" and "REATTRIBUTION TO SPOUSE" pop out as pretty strange.

It turns out that "redesignations" and "reattributions" are perfectly normal ([link](http://www.fec.gov/pages/brochures/contrib.shtml#Excessive_Contributions)).  If a donation by person A is excessive, the part that exceeds the limits can be "reattributed" to person B, meaning that person B donated the rest to the campaign.  Alternatively, the excess amount can be redesignated to another campaign in the same party.  So a donation to Obama could be redesignated to a poor democrat in Nebraska.

What's fishy is "REATTRIBUTION TO SPOUSE".  A quick google search tells us that this is a tactic to hide campaign contributions from corporate CEOs.  The CEO will donate money, which will be reattributed (refunded) to the CEO's spouse.  Then the humble spouse will turn around and donate the money to the candidate.  In this way, it's hard for a casual browser to notice that the candidate is backed by corporate CEOs. ([link](http://irregulartimes.com/index.php/archives/2010/11/28/corporate-executives-pawn-off-tim-pawlenty-contributions/))

The following exercises will ask you to compare Obama's donations with McCain's donations.

# Exercise 1: Plot Obama vs. McCain

Earlier, we only plotted Obama's campaign donations.  Modify the script to also plot McCain's donations on the same chart.  It should look something like:

<img src="./graph2.png" width="80%">

Whoa whoa whoa, what's McCain been up to March 2008?  That's a whole lot of negative donations!  We'll deal with that in a couple exercises.

# Exercise 2: Cumulative Graphs

Word on the street says that Obama's donations eclipsed McCain's donations.  Let's see if that's true.  Plot the cumulative donations (for a given date, plot the total donations up to that date).  It should look something like:

<img src="./graph3.png" width="80%"/>

# Exercise 3: Understand "Reattribution to Spouse"

Let's now filter the contributions to only see the cumulative "reattribution to spouse"" donations.  Which candidate do the dark, hooded CEOs prefer?  

You will need to find the name of the field that contains the "reattribution" text, and filter on that field.  Depending on how you filter it, you may get different results.  Try out a few to see what you'll get.

# Exercise 4: Zooming Out

Reality check.  If you saw the graph in the previous exercise, you would think "That's a lot of negative donations, this candidate is really sneaky".  Don't believe that just yet.  Re-plot the **ratio** of cumulative "reattribution to spouse" donations to the cumulative overall donations.  It's not even a blip on the radar.

**Key Lesson: don't automatically trust charts in the wild.  It's easy to make a chart say whatever you want by selectively leaving out data!**

# Done!

Congrats!  You are now a data sleuth.  To recap the process we just went through we:

1. Took a quick look at the data using `head` to get a sense of what we're dealing with.  We also figured out the format of the data.  This is usually important, because the fields are otherwise somewhat non-sensical!
1. Create a quick, initial visualization of some of the data fields and see if there are interesting trends.
1. Listen to your hunch, and form a hypothesis around it
1. Figure out why the trend exists
1. Filter the dataset to the "interesting portion" and go to step 2

Tomorrow, we will dive deeper into `matplotlib`'s visualization facilities, and further analyze the data using different visualizations.

