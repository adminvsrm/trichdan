# Script to extract list of journals, conferences, books from Scopus exported data, the list contain sources of papers and source of citations for papers of network authors
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_sources_net.py
# Output is file list_sources_net.csv
# Other way: python3 get_sources_net.py list_citations.csv output_file.csv input_net_authors.txt

import os
import sys
import csv_tools

    
## Main operation, when calling: python3 get_sources_net.py list_citations.csv output_file.csv input_net_authors.txt
if __name__ == "__main__":
    if len(sys.argv)>1:
        listCitations = str(sys.argv[1])
    else:
        listCitations = 'list_citations.csv'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_sources_citations_net.csv'
    if len(sys.argv)>3:
        listNetAuthors = str(sys.argv[3])
    else:
        listNetAuthors = 'input_net_authors.txt'

    #get_sources_citations_net(listCitations, exportFile, listNetAuthors)
    list_header = ['ID', 'Source title', 'Abbreviated Source Title', 'Publisher', 'Conference name', 'Rating']
    list_sources = [list_header]
    
    with open(listNetAuthors, "rt") as textfile:
        author_lines = textfile.readlines()
        filtered_authors = [x.strip() for x in author_lines if x.strip()]
    
    citeTable = csv_tools.read_csv_table(listCitations)
    headerTable = citeTable[0]
    # Note that header of citation table is ['ID', 'Number of citations in selected database', 'List ID of citations', 'Title', 'Authors', 'Source title', 'Abbreviated Source Title', 'Publisher', 'Conference name', 'Year', 'Link']


    processed_source = []
    
    author_index = headerTable.index('Authors')
    sourceTitle_index = headerTable.index('Source title')
    abbr_sourceTitle_index = headerTable.index('Abbreviated Source Title')
    publisher_index = headerTable.index('Publisher')
    conference_index = headerTable.index('Conference name')
    access_index = [sourceTitle_index, abbr_sourceTitle_index, publisher_index, conference_index]

    for row in citeTable[1:]:
        # Collect journal name of authors
        authors_split = row[author_index].split(',')
        list_authors = [author.strip() for author in authors_split]
        for author in list_authors:
            if author in filtered_authors:
                if not row[sourceTitle_index] in processed_source:
                    list_sources.append([row[k] for k in access_index])
                    processed_source.append(row[sourceTitle_index])
                        
        
                # Collect journal name of citations of authors
                paper_id = str(row[0])
                paper_cite = row[2].split(',')
                if not paper_cite == ['']: # there are some references in the list of papers
                    for citation in paper_cite:
                        source_cite = citeTable[int(citation)][sourceTitle_index]
                        if not source_cite in processed_source:
                            list_sources.append([citeTable[int(citation)][k] for k in access_index])
                            processed_source.append(source_cite)
                        

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

    