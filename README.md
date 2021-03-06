# SoftwareWebScrape

Webscraper for multiple json, https and XML public websites that publish software release version info, update info and release dates.  The script will scrape the following websites for the (softwares) in question:

https://vergrabber.kingu.pl/vergrabber.json (Google Chrome, Adobe Acrobat Reader and Adobe Acrobat Reader DC)
https://patchmypc.com/freeupdater/definitions/definitions.xml (Firefox and FirefoxESR)
https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/releases-index.json (DOTNet and DOTNet Core)
http://httpd.apache.org/download.cgi (Apache HTTP Server)
https://www.oracle.com/middleware/technologies/weblogic-server-installers-downloads.html (Oracle WebLogic Server)
https://www.qualys.com/documentation/release-notes/index.json (Qualys Cloud Agent for Linux and Windows)
https://docs.splunk.com/Documentation/Splunk/8.1.2/ReleaseNotes/MeetSplunk (Splunk)
https://github.com/corretto/corretto-8/releases (Amazon Corretto 8)
https://github.com/corretto/corretto-11/releases (Amazon Corretto 11)
https://github.com/corretto/corretto-JDK/releases (Amazon Corretto JDK)

Datefinder library was used for scraping the date from the oracle and splunk software sites due to no real identifiers being present. You will need to install datefinder prior to using: 

pip install datefinder

A single function was created for scraping the GitHub sites.  This function will apply to any GitHub, thus all that is needed is to pass the url and the correct version. 

