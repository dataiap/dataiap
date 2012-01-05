all: labs

labs: day0/README.md day1/README.md day2/README.md day3/regression.py day3/hypothesis_testing.py
	python resources/markdown/markdown_headers.py day0/README.md > /tmp/dataiap_html/day0.html
	python resources/markdown/markdown_headers.py day1/README.md > /tmp/dataiap_html/day1.html
	python resources/markdown/markdown_headers.py day2/README.md > /tmp/dataiap_html/day1.html
	python resources/hacco/hacco.py day3/regression.py -d /tmp/dataiap_html
	python resources/hacco/hacco.py day3/hypothesis_testing.py -d /tmp/dataiap_html