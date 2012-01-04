all: labs

labs: day1/README.md day2/README.md day3/regression.py day3/hypothesis_testing.py
	markdown_py day0/README.md > day0/index.html
	markdown_py day1/README.md > day1/index.html
	markdown_py day2/README.md > day2/index.html
	python resources/hacco/hacco.py day3/regression.py -d day3
	python resources/hacco/hacco.py day3/hypothesis_testing.py -d day3