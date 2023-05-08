from bs4 import BeautifulSoup
import csv
import zipfile
import os
import glob
import shutil
# import json

dictibanentries = {}
alltags = {}
ibanList = {}
filelist = []
ibandict = {}
mylist = []


def createcsv(headers, ibanlists):
    for iban in ibanList:
        with open('./downloads/' + iban + ".csv", 'w', newline='', encoding='utf-8') as f:
            filelist.append(iban)
            writer = csv.writer(f)
            writer.writerow(headers)
            for b in ibanlists[iban]:
                writer.writerow(b.values())

        # makejson(entries)


def makearchive():  # Create zip archive from files in download folder
    filename = "./archives/csvperiban"
    format = "zip"
    directory = "./downloads"
    shutil.make_archive(filename, format, directory)
    shutil.rmtree('./uploads/')
    shutil.rmtree('./downloads/')
    os.makedirs('./uploads')
    os.makedirs('./downloads')


# def makejson(entries):
#     for list in entries:
#         newlist = [x for x in list]
#         with open('filename', 'w', encoding='utf8') as json_file:
#             json.dump(newlist, json_file, ensure_ascii=False)


def getalltags():
    path = './uploads/'
    for filename in glob.glob(os.path.join(path, '*.zip')):
        with zipfile.ZipFile(os.path.join(os.getcwd(), filename), 'r') as zf:
            for name in zf.namelist():
                # Check for IBAN in filename
                soup = BeautifulSoup(zf.open(name), "xml")

                # Get all tags from input file and save it to list
                tags = [tag.name for tag in soup.find_all()]
                for tag in tags:
                    if not tag in alltags:
                        alltags[tag] = ""


def xml_parsing():  # parse input xmls, find all entries, tags and ibans. sort them and put in single directories
    # Import complete ZIP-Files
    path = './uploads/'
    for filename in glob.glob(os.path.join(path, '*.zip')):
        with zipfile.ZipFile(os.path.join(os.getcwd(), filename), 'r') as zf:
            for name in zf.namelist():
                soup = BeautifulSoup(zf.open(name), "xml")
                iban = soup.find('IBAN')
                x = iban.text
                ibanList.setdefault(x, [])
                dictibanentries.update({x: ""})
                getalltags()
                b_ntry = soup.find_all('Ntry')

                for ntry in b_ntry:
                    tagEntries = {}
                    for tag in alltags:
                        a = ntry.find(tag)
                        if a:
                            tagEntries[tag.title()] = a.text
                        else:
                            tagEntries[tag.title()] = ""
                    ibanList[x] += [tagEntries]
        createcsv(alltags, ibanList)
    makearchive()


# AKTUELL 08.05.2023 20:18
