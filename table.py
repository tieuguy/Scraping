from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://www.cadth.ca/about-cadth/what-we-do/products-and-services/pcodr/transparency/find-a-review")
soup = BeautifulSoup(html, "html.parser")

table_tag = soup.table
for child in table_tag.children.children:
	print (child)