# Script to extract papers from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_papers.py
# Output is file list_papers.csv
# Other way: python3 get_papers.py data_folder output_file.csv

import os
import sys
import csv_tools

    
## Main operation, when calling: python get_authors.py data_folder
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_papers.csv'

    #get_papers(dataFolder, exportFile)
    list_header = ['ID', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link']
    list_papers = [list_header]

    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Authors' in headerTable and 'Title' in headerTable and 'Year' in headerTable and 'Source title' in headerTable and 'DOI' in headerTable and 'Publisher' in headerTable:
                    title_index = headerTable.index('Title')
                    author_index = headerTable.index('Authors')
                    sourceTitle_index = headerTable.index('Source title')
                    publisher_index = headerTable.index('Publisher')
                    link_index = headerTable.index('DOI')
                    year_index = headerTable.index('Year')
                    access_index = [title_index, author_index, sourceTitle_index, publisher_index, year_index, link_index]
                    for row in table[1:]:
                        if not row[title_index] in [item[0] for item in list_papers]:
                            list_papers.append([row[k] for k in access_index])

    # This command should be executed after all the papers were collected
    del list_papers[0] # remove header line before sorting
    list_papers.sort(key=lambda x:x[0],reverse=False) # sort by title, note that ID column is not added yet
    list_papers.insert(0, list_header)
    for k in range(1, len(list_papers)):
        list_papers[k].insert(0, k) # add ID
    csv_tools.write_table_csv(exportFile, list_papers)
    #print(list_papers)

    