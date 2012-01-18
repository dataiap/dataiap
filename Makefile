all: labs

labs: day0/README.md day1/README.md day2/README.md day3/regression.py day3/hypothesis_testing.py
	cp  -r ./day0 ./day1 ./day2 ./day3 ./day4 ./day5 ./lectures /tmp/dataiap_html/
	rm /tmp/dataiap_html/lectures/*.pptx
	python resources/markdown/markdown_headers.py day0/README.md /tmp/dataiap_html/day0/index.html
	python resources/markdown/markdown_headers.py day1/README.md /tmp/dataiap_html/day1/index.html
	python resources/markdown/markdown_headers.py day2/README.md /tmp/dataiap_html/day2/index.html
	python resources/markdown/markdown_headers.py day3/README.md /tmp/dataiap_html/day3/index.html
	python resources/markdown/markdown_headers.py day4/README.md /tmp/dataiap_html/day4/index.html
	python resources/hacco/hacco.py day3/regression.py -d /tmp/dataiap_html/day3/ #/tmp/dataiap_html
	python resources/hacco/hacco.py day3/hypothesis_testing.py -d /tmp/dataiap_html/day3/ #/tmp/dataiap_html
	python resources/hacco/hacco.py day5/mapreduce.py -d /tmp/dataiap_html/day5/ #/tmp/dataiap_html
	echo "\n\nnow do: \n\tgit checkout gh-pages\n\tcp -r /tmp/dataiap_html/* .\n"
