mysearch = "gribble+pl"
retmax = 10

import urllib
from lxml import etree

searchURLbase = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=" + str(retmax) + "&term="
searchURL = searchURLbase + mysearch
page = urllib.urlopen(searchURL)
pagedata = page.read()
resXML = etree.XML(pagedata)
count = int(resXML.find("Count").text)
retmax = int(resXML.find("RetMax").text)
retstart = int(resXML.find("RetStart").text)
idlistXML = resXML.find("IdList")
idlist = [0]*retmax

for i in range(retmax):
	idlist[i] = idlistXML[i].text

fetchURLbase = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
fetchURL = fetchURLbase
for i in range(retmax):
	fetchURL = fetchURL + idlist[i]
	if (i<(retmax-1)):
		fetchURL = fetchURL + ","

artsreq = urllib.urlopen(fetchURL)
artsdat = artsreq.read()
artsXML = etree.XML(artsdat)

articleList=[]
for i in range(retmax):
	articleList = articleList + [{'title': artsXML[i].find("MedlineCitation").find("Article").find("ArticleTitle").text}]
	articleList[i]['journal_full'] = artsXML[i].find("MedlineCitation").find("Article").find("Journal").find("Title").text
	articleList[i]['journal_abbrev'] = artsXML[i].find("MedlineCitation").find("MedlineJournalInfo").find("MedlineTA").text
	articleList[i]['year'] = artsXML[i].find("MedlineCitation").find("Article").find("Journal").find("JournalIssue").find("PubDate").find("Year").text
	articleList[i]['pmid'] = artsXML[i].find("MedlineCitation").find("PMID").text
	tmp = artsXML[i].find("MedlineCitation").find("Article").find("Journal").find("JournalIssue").find("Volume")
	if not(tmp==None):
		articleList[i]['volume'] = tmp.text
	tmp = artsXML[i].find("MedlineCitation").find("Article").find("Journal").find("JournalIssue").find("Issue")
	if not(tmp==None):
		articleList[i]['issue'] = tmp.text
	tmp = artsXML[i].find("MedlineCitation").find("Article").find("Pagination").find("MedlinePgn")
	if not(tmp==None):
		articleList[i]['pages'] = tmp.text
	authorsXML = artsXML[i].find("MedlineCitation").find("Article").find("AuthorList")
	authorlist=[]
	for j in range(len(authorsXML)):
		authorlist = authorlist + [{'lastname': authorsXML[j].find("LastName").text}]
		authorlist[j]['firstname'] = authorsXML[j].find("ForeName").text
		authorlist[j]['initials'] = authorsXML[j].find("Initials").text
	articleList[i]['authors'] = authorlist


def printArticle(articleDict):
	printstr = ""
	for author in articleDict['authors']:
		printstr += author['lastname'] + " " + author['initials'] + ", "
	printstr = printstr[:-2] + " "
	printstr += "(" + articleDict['year'] + ") "
	printstr += articleDict['title'] + " "
	printstr += articleDict['journal_abbrev'] + " "
	if 'volume' in articleDict.keys():
		if type(articleDict['volume']) is str:
			printstr += articleDict['volume'] + ":"
	if 'pages' in articleDict.keys():
		if type(articleDict['pages']) is str:
			printstr += articleDict['pages']
	return printstr

print "\n"
for article in articleList:
	print printArticle(article) + "\n"



