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
tdArray = []
brArray = []

# create arrays for storing information
headings = ["Brand Name", "Generic Name", "Tumour Type", "Indication", "Review Status", "Last Updated"]
brandName = []
genericName = []
tumourType = []
indication = []
reviewStatus = []
lastUpdated = []

#find all the br stuff in the soup
brContent = soup.find("table", {"class" : "sortable_table"}).find_all("br")

# store the br info into an array
for child in brContent:
	brArray.append(child.string)

# remove all the br content from the soup
for e in soup.findAll('br'):
	e.extract()

# find all the td stuff in the soup
tdContent = soup.find("table", {"class" : "sortable_table"}).find_all("td")

# store the td info into an array
for child in tdContent:
	tdArray.append(child.string)

indication = brArray
# store information into arrays
while tdArray:
	brandName.append(tdArray.pop(0))
	genericName.append(tdArray.pop(0))
	tumourType.append(tdArray.pop(0))
	reviewStatus.append(tdArray.pop(0))
	lastUpdated.append(tdArray.pop(0))
"""
print(brandName)
print(genericName)
print(tumourType)
print(indication)
print(reviewStatus)
print(lastUpdated)
"""

# store information into an excel sheet
wb = xlwt.Workbook()
ws = wb.add_sheet('Drugs')
row = 1;
column = 0;

# titles / headings
for x in range(0, 6):
	ws.write(0, x, headings.pop(0))

# rest of the data
while brandName:
	ws.write(row, column + 0, brandName.pop(0))
	ws.write(row, column + 1, genericName.pop(0))
	ws.write(row, column + 2, tumourType.pop(0))
	ws.write(row, column + 3, indication.pop(0))
	ws.write(row, column + 4, reviewStatus.pop(0))
	ws.write(row, column + 5, lastUpdated.pop(0))
	row+=1

# save the excel file
wb.save("drugs.xls")
