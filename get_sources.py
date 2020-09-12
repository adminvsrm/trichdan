# Script to extract list of journals, conferences, books from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_sources.py
# Output is file list_journals.csv
# Other way: python3 get_sources.py data_folder output_file.csv

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
        exportFile = 'list_sources.csv'

    #get_papers(dataFolder, exportFile)
    list_header = ['ID', 'Source title', 'Abbreviated Source Title', 'Publisher', 'Conference name', 'Rating']
    list_sources = [list_header]
    processed_source = []

    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                print('Processing file ' + csvFile)
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Source title' in headerTable and 'Abbreviated Source Title' in headerTable and 'Publisher' in headerTable and 'Conference name' in headerTable:
                    sourceTitle_index = headerTable.index('Source title')
                    abbr_sourceTitle_index = headerTable.index('Abbreviated Source Title')
                    publisher_index = headerTable.index('Publisher')
                    conference_index = headerTable.index('Conference name')
                    access_index = [sourceTitle_index, abbr_sourceTitle_index, publisher_index, conference_index]
                for row in table[1:]:
                    if not row[sourceTitle_index] in processed_source:
                        list_sources.append([row[k] for k in access_index])
                        processed_source.append(row[sourceTitle_index])

    # This command should be executed after all the papers were collected
    del list_sources[0] # remove header line before sorting
    list_sources.sort(key=lambda x:x[0],reverse=False) # sort by title, note that ID column is not added yet
    list_sources.insert(0, list_header)
    for k in range(1, len(list_sources)):
        list_sources[k].insert(0, k) # add ID
        list_sources[k].append('') # add blank column for Rating
    csv_tools.write_table_csv(exportFile, list_sources)
    #print(list_sources)
    print('Analysis finished. Result is written to file ' + exportFile)

    