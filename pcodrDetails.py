# BeautifulSoup is used to obtain the html document and for parsing
from bs4 import BeautifulSoup
# urllib.request for Python 3, urllib for Python 2
from urllib.request import urlopen
# xlwt is used to port the data to an excel sheet
import xlwt

url = "https://www.cadth.ca/about-cadth/what-we-do/products-and-services/pcodr/transparency/find-a-review"

# set url to scrape from
html = urlopen(url)
#soup = str(html.read(), 'utf-8')
# create soup
soup = BeautifulSoup(html, "html.parser")

# create arrays for extracting information
linkArray = []
pcodrValueArray =[]
tdArray = []

# find all the links
for link in soup.find("table", {"class" : "sortable_table"}).find_all('a'):
	linkArray.append(link.get('href'))

# find all the td
for child in soup.find("table", {"class" : "sortable_table"}).find_all('td'):
	tdArray.append(child.string)

# remove everything except for "Last Updated" data
ctr = 0
for x in tdArray:
	tdArray.pop(ctr)
	tdArray.pop(ctr)
	tdArray.pop(ctr)
	tdArray.pop(ctr)
	ctr += 1

# create arrays for storing information
headings = ["Brand Name", "Generic Name", "Strength", "Tumour Type", "Indication", "Funding Request", 
"Review Status", "Pre Noc Submission", "NOC Date", "Manufacturer", "Submitter", "Submission Date", 
"Submission Deemed Complete", "Submission Type", "Prioritization Requested", 
"Patient Advocacy Group Input Deadline", "Check-point meeting", "pERC Meeting", "Initial Recommendation Issued", 
"Feedback Deadline", "pERC Reconsideration Meeting", "Final Recommendation Issued", 
"Notification to Implement Issued", "Last Updated"]

# set up excel workbook and sheet for information storage
wb = xlwt.Workbook()
# enabling cell_overwrite_ok for special case 5 pertaining to NOC/c written into NOC cell
ws = wb.add_sheet('Drugs', cell_overwrite_ok=True)
row = 1;
column = 0;

# titles / headings
for x in range(0, len(headings)):
	ws.write(0, x, headings[x])

for relativeLink in linkArray:
	innerurl = "https://www.cadth.ca" + relativeLink
	# NOTE: urlopen may fail if site notices quick successive demands from single point (scraping)
	#		solution: wait a bit in-between accesses
	innerhtml = urlopen(innerurl)
	innerSoup = BeautifulSoup(innerhtml, "html.parser")

	# find all the th stuff in the innerSoup
	pcodrHeaderArray = innerSoup.find("table", {"class" : "pcodr_table"}).find_all("th")
	# find all the td stuff in the innerSoup
	pcodrValueArray = innerSoup.find("table", {"class" : "pcodr_table"}).find_all("td")

	# go through each of the headings and store the appropriate data
	for x in headings:
		# the "Last Updated" heading is updated with data from tdArray
		if x == "Last Updated":
			ws.write(row, headings.index(x), tdArray.pop(0))
			continue
		# break if there is no more data from innerlink
		if not pcodrHeaderArray:
			break
		# cases where the headings don't match up
		if x != pcodrHeaderArray[0].string[:len(x)]:
			# case 1: skip over "Clarification" headings
			if pcodrHeaderArray[0].string == "Clarification":
				pcodrHeaderArray.pop(0)
				pcodrValueArray.pop(0)
			# case 2: missing "pERC Reconsideration Meeting"
			elif x == "pERC Reconsideration Meeting":
				continue
			# case 3: missing "Strength"
			elif x == "Strength" and pcodrHeaderArray[0].string == "Tumour Type":
				continue
			# case 4: missing "Submission Deemed Complete"
			elif x == "Submission Deemed Complete" and pcodrHeaderArray[0].string == "Submission Type":
				continue
			# case 5: put in the "NOC/c Date" into the "NOC Date" heading
			elif pcodrHeaderArray[0].string == "NOC/c Date":
				pcodrHeaderArray.pop(0)
				ws.write(row, headings.index("NOC Date"), pcodrValueArray.pop(0).string)

		pcodrHeaderArray.pop(0)
		ws.write(row, headings.index(x), pcodrValueArray.pop(0).string)

	row+=1

# save the excel file
wb.save("newDrugs.xls")
