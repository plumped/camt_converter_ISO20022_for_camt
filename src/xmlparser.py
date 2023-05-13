from bs4 import BeautifulSoup
from collections import defaultdict
import csv
import zipfile
import os
import glob
import shutil

# A dictionary to store all the tags found in the input files
alltags = {}

allFiles = []

# A dictionary with IBAN as the key and list of entries as the value
ibanList = defaultdict(list)

# Method to create a CSV file for each IBAN


def create_csv(headers):
    # Iterate over all IBANs and their entries
    for iban, entries in ibanList.items():
        # Create a CSV file with the name of the IBAN
        allFiles.append(iban)
        with open(f'./downloads/{iban}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write the headers for the CSV file
            writer.writerow(headers)
            # Write each entry as a row in the CSV file
            for entry in entries:
                writer.writerow(entry.values())


def clear_parsed_files():
    allFiles.clear()


def clear_iban_list():
    ibanList.clear()


def get_parsed_files():
    return allFiles

# Method to create a zip archive of all CSV files in the downloads folder


def make_archive():
    # Set the name of the archive file
    filename = "./archives/csvperiban"
    # Set the format of the archive file
    format = "zip"
    # Set the directory containing the CSV files to be archived
    directory = "./downloads"
    # Create the archive file
    shutil.make_archive(filename, format, directory)
    # Remove the uploads and downloads folders
    shutil.rmtree('./uploads/')
    shutil.rmtree('./downloads/')
    # Recreate the uploads and downloads folders
    os.makedirs('./uploads')
    os.makedirs('./downloads')


def get_all_tags():
    # set the path of the upload directory
    path = './uploads/'
    # set an empty set to store the tags that are already seen
    seen_tags = set()
    # loop over each .zip file in the upload directory
    for filename in glob.glob(os.path.join(path, '*.zip')):
        # read the content of the .zip file
        with zipfile.ZipFile(os.path.join(os.getcwd(), filename), 'r') as zf:
            # loop over each file in the .zip archive
            for name in zf.namelist():
                # parse the XML file with BeautifulSoup
                soup = BeautifulSoup(zf.open(name), 'xml')
                # find all the tags in the XML file
                tags = [tag.name for tag in soup.find_all()]
                # add new tags to the dictionary of all tags
                for tag in sorted(tags):
                    if tag not in seen_tags:
                        alltags[tag] = ''
                        seen_tags.add(tag)


def parse_xml_files():
    # set path and get all tags
    clear_iban_list()
    path = './uploads/'
    get_all_tags()
    # iterate through zip files in uploads directory
    for filename in glob.glob(os.path.join(path, '*.zip')):
        with zipfile.ZipFile(os.path.join(os.getcwd(), filename), 'r') as zf:
            # iterate through xml files in the zip
            for name in zf.namelist():
                # parse the xml file with BeautifulSoup
                soup = BeautifulSoup(zf.open(name), 'xml')
                iban = soup.find('IBAN')
                x = iban.text
                b_ntry = soup.find_all('Ntry')
                for ntry in b_ntry:
                    tag_entries = {}
                    # iterate through all tags and find matching entries in xml file
                    for tag in alltags:
                        a = ntry.find(tag)
                        if tag == 'Cdtr':
                            tag_entries[tag.title()] = a.find('Nm').text if a and a.find('Nm') else ''
                        elif tag == 'Dbtr':
                            tag_entries[tag.title()] = a.find('Nm').text if a and a.find('Nm') else ''
                        else:
                            tag_entries[tag.title()] = a.text if a else ''
                    ibanList[x].append(tag_entries)
            zf.close()
        create_csv(alltags)
    make_archive()