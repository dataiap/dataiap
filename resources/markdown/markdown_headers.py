import codecs
import markdown
import sys

input_file = codecs.open(sys.argv[1], mode="r", encoding="utf8", errors="ignore") #open(sys.argv[1])
html = markdown.markdown(input_file.read())
html = """
<html>
<head>
<title>Data IAP Day 1</title>
<link rel="stylesheet" type="text/css" href="clearness.css"/>
</head>
<body>
%s
</body>
</html>
""" % (html)

print html
