all: labs

labs: day0/README.md day1/README.md day2/README.md day3/regression.py day3/hypothesis_testing.py
	python resources/markdown/markdown_headers.py day0/README.md day0/index.html
	python resources/markdown/markdown_headers.py day1/README.md day1/index.html
	python resources/markdown/markdown_headers.py day2/README.md day2/index.html
	python resources/markdown/markdown_headers.py day4/README.md day4/index.html
	python resources/hacco/hacco.py day3/regression.py -d day3/ #/tmp/dataiap_html
	python resources/hacco/hacco.py day3/hypothesis_testing.py -d day3/ #/tmp/dataiap_html
	cp  -r ./day0 ./day1 ./day2 ./day3 ./day4 /tmp/dataiap_html/
	echo "\n\nnow do: \n\tgit checkout gh-pages\n\tcp -r /tmp/dataiap_html/* .\n"