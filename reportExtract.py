# BeautifulSoup is used to obtain the html document and for parsing
from bs4 import BeautifulSoup
# urllib.request for Python 3, urllib for Python 2
from urllib.request import urlopen
# xlwt is used to port the data to an excel sheet
import xlwt

url = "https://www.cadth.ca/about-cadth/what-we-do/products-services/cdr/reports"


# set url to scrape from
html = urlopen(url)
#soup = str(html.read(), 'utf-8')
# create soup
soup = BeautifulSoup(html, "html.parser")

# create arrays for extracting information
tdArray = []

# create arrays for storing information
headings = ["Brand Name", "Generic Name", "Indication", "Project Status", "Date Submission Received", "Date Recommendation Issued"]
brandName = []
genericName = []
indication = []
projectStatus = []
dsr = []
dri = []

# find all the td stuff in the soup
tdContent = soup.find("table", {"class" : "sortable_table"}).find_all("td")

# store the td info into an array
for child in tdContent:
	tdArray.append(child.string)

# store information into arrays
while tdArray:
	brandName.append(tdArray.pop(0))
	genericName.append(tdArray.pop(0))
	indication.append(tdArray.pop(0))
	projectStatus.append(tdArray.pop(0))
	dsr.append(tdArray.pop(0))
	dri.append(tdArray.pop(0))
"""
print(brandName)
print(genericName)
print(indication)
print(projectStatus)
print(dsr)
print(dri)
"""

# store information into an excel sheet
wb = xlwt.Workbook()
ws = wb.add_sheet('Reports')
row = 1;
column = 0;

# titles / headings
for x in range(0, 6):
	ws.write(0, x, headings.pop(0))

# rest of the data
while brandName:
	ws.write(row, column + 0, brandName.pop(0))
	ws.write(row, column + 1, genericName.pop(0))
	ws.write(row, column + 2, indication.pop(0))
	ws.write(row, column + 3, projectStatus.pop(0))
	ws.write(row, column + 4, dsr.pop(0))
	ws.write(row, column + 5, dri.pop(0))
	row+=1

# save the excel file
wb.save("reports.xls")
