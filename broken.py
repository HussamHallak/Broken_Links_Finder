import sys
from bs4 import BeautifulSoup
import urllib2
import re

if len(sys.argv) != 2:
	print "Usage: Python extracrPDF.py <url>"
	print "e.g: Python extracrPDF.py http://example.com/page.html"
else:
	url = sys.argv[1]
	html_page = urllib2.urlopen(url)
	# The output file is named after the url with minor modifications, to be accepted by the operating system, in order to maintain unique output file names
	file_name = str(url)
	file_name = file_name + ".broken.txt"
	file_name = file_name.replace("http://", "")
	file_name = file_name.replace("https://","")
	file_name = file_name.replace("/","_SLASH_")
	file = open(file_name,"w")	
	file.write("From the page:")
	file.write("\n")
	file.write(html_page.geturl())
	file.write("\n")
	file.write("*******************")
	file.write("\n")
	soup = BeautifulSoup(html_page, "html.parser")
	links = []
	#You can add as many error codes as you want to this list. Error codes include: 
	# 404 Not Found, 400 Bad request, 403 Forbidden, 301 Moved Permanently, 204 No Content,...etc
	error_codes = [404, 400, 403, 301, 204]
	for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
		links.append(link.get('href'))
	counter = 1
	for link in links:
		try:
			r = urllib2.urlopen(link)
		except urllib2.HTTPError as e:
			file.write(str(counter))
			file.write(". ")
			file.write("This link produced an error:")
			file.write("\n")
			file.write(link)
			file.write("\n")
			file.write("-----------------------------")
			file.write("\n")
			counter = counter + 1
	file.close()
