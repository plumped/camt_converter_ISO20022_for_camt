from bs4 import BeautifulSoup
import csv

# Reading the data inside the xml
# file to a variable under the name
# data
with open('xml_files/test.xml', 'r') as f:
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
soup = BeautifulSoup(data, "xml")

# Define variables for splitting data input into structured packages
b_entries_all = soup.find_all()
b_entries_ntry = soup.find_all('Ntry')
b_entries_sumup = soup.find_all('TtlNtries')

# Get all tags from input file and save it to list
allTags = [tag.name for tag in soup.find_all()]

# Iterate through all tags and save tag.name and tag.value in dictionary
# Save all dictionaries in a list
entriesList= []
for ntry in b_entries_ntry:
    tagEntries = {}
    for tag in allTags:
        a = ntry.find((tag))
        if a:
            tagEntries[tag.title()] = a.text
    entriesList.append(tagEntries)
for a in entriesList:
    print(a)

sumup = []
for ntry in b_entries_sumup:
    d = {
        'Total transaction amount in this report: ' + ntry.find_next('Amt').string,
        'Number of entries in this report: ' + ntry.find_next('NbOfNtries').string,
    }
    sumup.append(d)
    print(d)
