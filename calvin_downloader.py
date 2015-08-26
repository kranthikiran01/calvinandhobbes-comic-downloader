import urllib2,urllib
import os
import datetime
from HTMLParser import HTMLParser

if not os.path.exists("calvinandhobbes"):
	os.makedirs("calvinandhobbes")

proxies={'http':"http://172.30.0.12:3128/",'https':"https://172.30.0.12:3128/"}
#Uncomment below line if you are not behind a proxy
#proxies={}
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
day=datetime.datetime.now()

print "Enter from year:"
year=int(raw_input())

while True:
	print "Enter to date: "
	c=int(raw_input("Enter to 0 to select today's date. Enter 1 to select custom date"))
	if c==0:
		day=datetime.datetime.now()
		break
	elif c==1:
		d=int(raw_input("Enter day:"))
		m=int(raw_input("Enter month: (in number)"))
		y=int(raw_input("Enter year:"))
		day=datetime.datetime(y,m,d,0,0)
		break
	else:
		print "Invalid choice. Enter again!"
class ImgErrException(Exception):
    pass

class MyHTMLParser(HTMLParser):
			imageURL=""
			def handle_starttag(self,tag,attrs):
				if tag=="img":
					keys = ('value','label')
					attr_dict=dict(attrs)
					for k,v in attr_dict.items():
						if k=="class":
							if "assets.amuniversal.com" in attr_dict['src'] and "strip" in attr_dict["class"] and attr_dict["alt"].lower() in attr_dict['src'].lower():
								MyHTMLParser.imageURL=attr_dict['src']

while day.year!=year:
	response = opener.open("http://www.gocomics.com/calvinandhobbes/"+str(day.strftime("%Y/%m/%d")))
	if not response.getcode()==200:
		print "Error 404: Image not found"
	else:
		content=response.read()

		parser = MyHTMLParser()

		parser.feed(content)

		try:
			saveImage=opener.open(parser.imageURL,timeout=5)
		except urllib2.URLError,e:
			if isinstance(e.reason, socket.timeout):
				print type(e)
				raise ImgErrException("There was an error: %r" % e)
		writeImage=open("calvinandhobbes/"+str(day.strftime("%B-%d-%Y").lower()),'wb')
		writeImage.write(saveImage.read())
		writeImage.close()
		print "Image saved!"
	day=day-datetime.timedelta(days=1)

print "Finished downloading!"
print "Sit back and enjoy reading comic strips!"