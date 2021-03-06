import json
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import datefinder


def vergrabber(jsonOutput):
	r=requests.get("https://vergrabber.kingu.pl/vergrabber.json")
	jsonData=r.json()
	
	#get products server side
	for software in jsonData["server"]:
		if software!="OpenSSL":
			continue
		for version in jsonData["server"][software]:
			softwareVersion=jsonData["server"][software][version]
			if softwareVersion["latest"]:
				obj={'Software':softwareVersion["product"],'Version':softwareVersion["edition"],'UpdateLevel':softwareVersion["version"],'ReleaseDate':softwareVersion["released"]}
				jsonOutput.append(obj)

	#get products client side
	for software in jsonData["client"]:
		if software!="Java" and software!="Google Chrome" and software!="Adobe Acrobat Reader":
			continue
		for version in jsonData["client"][software]:
			if software=="Adobe Acrobat Reader" and version !="DC 2021":
				continue
			softwareVersion=jsonData["client"][software][version]
			if softwareVersion["latest"]:
				obj={'Software':softwareVersion["product"],'Version':softwareVersion["edition"],'UpdateLevel':softwareVersion["version"],'ReleaseDate':softwareVersion["released"]}
				jsonOutput.append(obj)


def patchmypc(jsonOutput):
	xmlString=requests.get("https://patchmypc.com/freeupdater/definitions/definitions.xml").text
	root = ET.fromstring(xmlString)
	FirefoxName = root.find(".//FirefoxName").text 
	FirefoxLabel = root.find(".//FirefoxLabel").text.split()[-1]
	FirefoxVer = root.find(".//FirefoxVer").text
	FirefoxESRLabel = root.find(".//FirefoxESRLabel").text.split()[-1]
	FirefoxESRName = root.find(".//FirefoxESRLabel").text.replace(FirefoxESRLabel,"")
	FirefoxESRVer = root.find(".//FirefoxESRVer").text
	obj1={'Software':FirefoxName,'Version':FirefoxLabel,'UpdateLevel':FirefoxVer,'ReleaseDate':'Latest'}
	obj2={'Software':FirefoxESRName,'Version':FirefoxESRLabel,'UpdateLevel':FirefoxESRVer,'ReleaseDate':'Latest'}
	jsonOutput.append(obj1)
	jsonOutput.append(obj2)


def dotnetcli(jsonOutput):
	r=requests.get("https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/releases-index.json")
	jsonData=r.json()
	NET={}
	NETCORE={}
	for release in jsonData["releases-index"]:
		#get the most recent .NET
		if release["product"]==".NET":
			if not NET:
				NET={'Software':release["product"],'Version':release["channel-version"],'UpdateLevel':release["latest-release"],'ReleaseDate':release["latest-release-date"]}
			if release["latest-release-date"]>NET["ReleaseDate"]:
				NET={'Software':release["product"],'Version':release["channel-version"],'UpdateLevel':release["latest-release"],'ReleaseDate':release["latest-release-date"]}
		#get the most recent .NET core
		if release["product"]==".NET Core":
			if not NETCORE:
				NETCORE={'Software':release["product"],'Version':release["channel-version"],'UpdateLevel':release["latest-release"],'ReleaseDate':release["latest-release-date"]}
			if release["latest-release-date"]>NETCORE["ReleaseDate"]:
				NETCORE={'Software':release["product"],'Version':release["channel-version"],'UpdateLevel':release["latest-release"],'ReleaseDate':release["latest-release-date"]}
	jsonOutput.append(NET)
	jsonOutput.append(NETCORE)


def github(jsonOutput,url,version):
	r=requests.get(url)
	soup= BeautifulSoup(r.content,'html.parser')
	software=soup.find("a",{'data-pjax':'#js-repo-pjax-container'}).text
	UpdateLevel=soup.find("div",{'class':'d-flex flex-items-start'}).text.split()[0]
	releaseDate=soup.find("relative-time")["datetime"].split("T")[0]
	obj={'Software':software,'Version':version,'UpdateLevel':UpdateLevel,'ReleaseDate':releaseDate}
	jsonOutput.append(obj)


def oracle(jsonOutput):
	r=requests.get("https://www.oracle.com/middleware/technologies/weblogic-server-installers-downloads.html")
	soup= BeautifulSoup(r.content,'html.parser')
	version=soup.findAll("h4")[1].text.split("Oracle WebLogic Server")[1].split()[0].strip()
	UpdateLevel=re.search('\(([^)]+)', soup.findAll("h4")[1].text).group(1)
	r1=requests.get("https://en.wikipedia.org/wiki/Oracle_WebLogic_Server")
	soup1= BeautifulSoup(r1.content,'html.parser')
	releaseDateStr=soup1.select(".mw-parser-output > ul:nth-of-type(1) li:nth-of-type(1)")[0].text.replace(".","")
	releaseDate=list(datefinder.find_dates(releaseDateStr))[0]
	releaseDateStr=releaseDate.strftime("%Y-%m-%d")
	obj={'Software':"Oracle WebLogic Server",'Version':version,'UpdateLevel':UpdateLevel,'ReleaseDate':releaseDateStr}
	jsonOutput.append(obj)


def apache(jsonOutput):
	r=requests.get("http://httpd.apache.org/download.cgi")
	soup= BeautifulSoup(r.content,'html.parser')
	version=soup.findAll("a",{'href':'#apache24'})[0].text.strip()[:3]
	UpdateLevel=soup.findAll("a",{'href':'#apache24'})[0].text.strip()
	releaseDate=re.search('\(([^)]+)', soup.find("div",{'id':'apcontents'}).findAll("li")[0].text).group(1).split()[-1]
	obj={'Software':"Apache HTTP Server",'Version':version,'UpdateLevel':UpdateLevel,'ReleaseDate':releaseDate}
	jsonOutput.append(obj)

def qualys(jsonOutput):
	r=requests.get("https://www.qualys.com/documentation/release-notes/index.json")
	jsonData=r.json()
	linux={}
	windows={}
	for release in jsonData:
		if "Cloud Agent Linux" in release['name']:
			if not linux:
				linux={'Software':'Qualys '+release["name"].rsplit(' ', 1)[0],'Version':release["name"].split()[-1].strip()[:3],'UpdateLevel':release["name"].split()[-1],'ReleaseDate':release["date"]}
			if release["date"]>linux["ReleaseDate"]:
				linux={'Software':'Qualys '+release["name"].rsplit(' ', 1)[0],'Version':release["name"].split()[-1].strip()[:3],'UpdateLevel':release["name"].split()[-1],'ReleaseDate':release["date"]}

		if "Cloud Agent Windows" in release['name']:
			if not windows:
				windows={'Software':'Qualys '+release["name"].rsplit(' ', 1)[0],'Version':release["name"].split()[-1].strip()[:3],'UpdateLevel':release["name"].split()[-1],'ReleaseDate':release["date"]}
			if release["date"]>windows["ReleaseDate"]:
				windows={'Software':'Qualys '+release["name"].rsplit(' ', 1)[0],'Version':release["name"].split()[-1].strip()[:3],'UpdateLevel':release["name"].split()[-1],'ReleaseDate':release["date"]}
	
	jsonOutput.append(linux)
	jsonOutput.append(windows)

def splunk(jsonOutput):
	r=requests.get("https://docs.splunk.com/Documentation/Splunk/8.1.2/ReleaseNotes/MeetSplunk")
	soup= BeautifulSoup(r.content,'html.parser')
	version=soup.find("h1").text.split()[-1]
	UpdateLevel=r.url.split("/")[5]
	releaseDateStr=soup.find("div",{'class':'mw-parser-output'}).text.replace(".","").split("first released on")[1]
	releaseDate=list(datefinder.find_dates(releaseDateStr))[0]
	releaseDateStr=releaseDate.strftime("%Y-%m-%d")
	obj={'Software':"Splunk",'Version':version,'UpdateLevel':UpdateLevel,'ReleaseDate':releaseDateStr}
	jsonOutput.append(obj)

jsonOutput=[]

try:
	qualys(jsonOutput)
	print("\n https://www.qualys.com/documentation/release-notes/   : success")
except:
	print("\n https://www.qualys.com/documentation/release-notes/   : failed")

try:
	vergrabber(jsonOutput)
	print("\n https://vergrabber.kingu.pl/vergrabber.json   : success")
except:
	print("\n https://vergrabber.kingu.pl/vergrabber.json   : failed")

try:
	patchmypc(jsonOutput)
	print("\n https://patchmypc.com/freeupdater/definitions/definitions.xml   : success")
except:
	print("\n https://patchmypc.com/freeupdater/definitions/definitions.xml   : failed")

try:
	dotnetcli(jsonOutput)
	print("\n https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/releases-index.json   : success")
except:
	print("\n https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/releases-index.json   : failed")
	
try:
	github(jsonOutput,"https://github.com/corretto/corretto-8/releases","8")
	print("\n https://github.com/corretto/corretto-8/releases   : success")
except:
	print("\n https://github.com/corretto/corretto-8/releases   : failed")
	
try:
	github(jsonOutput,"https://github.com/corretto/corretto-11/releases","11")
	print("\n https://github.com/corretto/corretto-11/releases   : success")
except:
	print("\n https://github.com/corretto/corretto-11/releases   : failed")
	
try:
	github(jsonOutput,"https://github.com/corretto/corretto-JDK/releases","15")
	print("\n https://github.com/corretto/corretto-JDK/releases   : success")
except:
	print("\n https://github.com/corretto/corretto-JDK/releases   : failed")
	
try:
	oracle(jsonOutput)
	print("\n https://www.oracle.com/middleware/technologies/weblogic-server-installers-downloads.html   : success")
except:
	print("\n https://www.oracle.com/middleware/technologies/weblogic-server-installers-downloads.html   : failed")


try:
	apache(jsonOutput)
	print("\n http://httpd.apache.org/download.cgi   : success")
except:
	print("\n http://httpd.apache.org/download.cgi   : failed")
	

try:
	splunk(jsonOutput)
	print("\n https://docs.splunk.com/Documentation/Splunk/8.1.2/ReleaseNotes/MeetSplunk   : success")
except:
	print("\n https://docs.splunk.com/Documentation/Splunk/8.1.2/ReleaseNotes/MeetSplunk   : failed")	

with open('output.json', 'w') as outfile:
    json.dump(jsonOutput, outfile, sort_keys=False, indent=4)
