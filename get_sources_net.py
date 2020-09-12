# Script to extract list of journals, conferences, books from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_sources_net.py
# Output is file list_sources_net.csv
# Other way: python3 get_sources_net.py data_folder output_file.csv input_net_authors.txt

import os
import sys
import csv_tools

    
## Main operation, when calling: python3 get_sources_net.py data_folder output_file.csv input_net_authors.txt
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_sources_net.csv'
    if len(sys.argv)>3:
        listNetAuthors = str(sys.argv[3])
    else:
        listNetAuthors = 'input_net_authors.txt'

    #get_papers(dataFolder, exportFile)
    list_header = ['ID', 'Source title', 'Abbreviated Source Title', 'Publisher', 'Conference name', 'Rating']
    list_sources = [list_header]
    
    with open(listNetAuthors, "rt") as textfile:
        author_lines = textfile.readlines()
        filtered_authors = [x.strip() for x in author_lines if x.strip()]

    processed_source = []

    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                print('Processing file ' + csvFile)
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Authors' in headerTable and 'Source title' in headerTable and 'Abbreviated Source Title' in headerTable and 'Publisher' in headerTable and 'Conference name' in headerTable:
                    author_index = headerTable.index('Authors')
                    sourceTitle_index = headerTable.index('Source title')
                    abbr_sourceTitle_index = headerTable.index('Abbreviated Source Title')
                    publisher_index = headerTable.index('Publisher')
                    conference_index = headerTable.index('Conference name')
                    access_index = [sourceTitle_index, abbr_sourceTitle_index, publisher_index, conference_index]
                    for row in table[1:]:
                        if not row[sourceTitle_index] in processed_source:
                            authors_split = row[author_index].split(',')
                            list_authors = [author.strip() for author in authors_split]
                            flag_author_exist = False
                            for author in list_authors:
                                print(author)
                                if author in filtered_authors:
                                    flag_author_exist = True
                            if flag_author_exist:
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

    