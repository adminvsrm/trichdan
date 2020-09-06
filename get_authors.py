# Script to parse authors and affiliations from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_authors.py
# Output is file list_all_authors.csv
# Other way: python3 get_authors.py data_folder output_file.csv

import os
import sys
import csv_tools


def export_table_combined(list_author_combined, list_affi_combined):
    table_combined = [[list_author_combined[k], len(list_affi_combined[k]), ';'.join(list_affi_combined[k])] for k in range(len(list_author_combined))]
    return table_combined
    
def group_affi_by_author(list_separate):
    list_author = []
    list_affi = []
    for item in list_separate:
        parse_item = parse_author_affi(item)
        fullname = parse_item['lastname'] + ' ' + parse_item['firstname']
        if fullname in list_author:
            index = list_author.index(fullname)
            list_affi[index].append(parse_item['affiliation'])
        else:
            list_author.append(fullname)
            list_affi.append([parse_item['affiliation']])
    return list_author, list_affi
        


def parse_author_affi(author_affi_text):
    # Parse the Authors with affiliations for each article
    # Example text: Ma, H.-B., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China; Zhuo, W.-D., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China
    lastname = author_affi_text[0:author_affi_text.find(',')]
    author_affi_text = author_affi_text[author_affi_text.find(',')+1:].lstrip()
    firstname = author_affi_text[0:author_affi_text.find(',')]
    affiliation = author_affi_text[author_affi_text.find(',')+1:].lstrip()
    
    return {'lastname': lastname, 'firstname': firstname, 'affiliation': affiliation}


def parse_author_affi_raw(author_affi_text):
    # Parse the Authors with affiliations for each article
    # Example text: Ma, H.-B., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China; Zhuo, W.-D., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China; Lavorato, D., Department of Architecture, Roma Tre University, Roma, 00154, Italy; Nuti, C., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China, Department of Architecture, Roma Tre University, Roma, 00154, Italy; Fiorentino, G., Department of Architecture, Roma Tre University, Roma, 00154, Italy; Marano, G.C., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China, College of Civil Engineering and Architecture, Politecnico di Bari University, Bari, 70126, Italy; Greco, R., College of Civil Engineering and Architecture, Politecnico di Bari University, Bari, 70126, Italy; Briseghella, B., College of Civil Engineering, Fuzhou University, Fuzhou, 350108, China
    list_authors = author_affi_text.split(';')
    list_parsed = []
    for author in list_authors:
        lastname = author[0:author.find(',')]
        author = author[author.find(',')+1:].lstrip()
        firstname = author[0:author.find(',')]
        affiliation = author[author.find(',')+1:].lstrip()
        list_parsed.append({'lastname': lastname, 'firstname': firstname, 'affiliation': affiliation})
    
    return list_parsed
    
## Main operation, when calling: python get_authors.py data_folder
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_all_authors.csv'

    #get_authors(dataFolder, exportFile)
    list_author_affi = []

    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Authors with affiliations' in headerTable:
                    affi_index = headerTable.index('Authors with affiliations')
                    affi_data = [row[affi_index] for row in table]
                    for paper_affi in affi_data[1:]:
                        list_authors = paper_affi.split(';')
                        for author in list_authors:
                            if not author.strip() in list_author_affi: # compare both name and affiliation
                                list_author_affi.append(author.strip())                

    # This command should be executed after all the author affiliations were collected
    list_author_affi.sort()
    list_author_combined, list_affi_combined = group_affi_by_author(list_author_affi)
    authorTable = export_table_combined(list_author_combined, list_affi_combined)
    list_header = ['Author', 'Number of affiliations', 'Affiliations']
    authorTable.insert(0, list_header)
    csv_tools.write_table_csv(exportFile, authorTable)


## Test with one file
#if __name__ == "__main__":
    #csvFile = 'TimonRabczuk_citation_by_authors.csv'
    #exportFile = 'list_all_authors.csv'
    #list_author_affi = []
    ## For each CSV file
    #table = csv_tools.read_csv_table(csvFile)
    #headerTable = table[0]
    #if 'Authors with affiliations' in headerTable:
        #affi_index = headerTable.index('Authors with affiliations')
        #affi_data = [row[affi_index] for row in table]
        ##print('List of authors and affiliations: \n')
        ##print(affi_data[1922])
        ##test = parse_author_affi(affi_data[1922])
        ##print(test['firstname'], test['lastname'], test['affiliation'])
    
        #for paper_affi in affi_data:
            #list_authors = paper_affi.split(';')
            #for author in list_authors:
                #if not author in list_author_affi: # compare both name and affiliation
                    #list_author_affi.append(author)                
    
        ## This command should be executed after all the author affiliations were collected
        #list_author_affi.sort()
        #list_author_combined, list_affi_combined = group_affi_by_author(list_author_affi)
        #authorTable = export_table_combined(list_author_combined, list_affi_combined)
        #csv_tools.write_table_csv(exportFile, authorTable)
        #print(authorTable)

    