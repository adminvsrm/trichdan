# Script to extract citations from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, run get_papers.py, then get_references.py, then run command: python3 get_citations.py
# Output is file list_citations.csv
# Other way: python3 get_citations.py data_folder output_file.csv list_of_references.csv

import os
import sys
import csv_tools
import re


## Main operation, when calling: python get_authors.py data_folder
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_citations.csv'
    if len(sys.argv)>3:
        listReferences = str(sys.argv[3])
    else:
        listReferences = 'list_references.csv'

    #get_citations(dataFolder, exportFile, listReferences)
    list_header = ['ID', 'Number of citations in selected database', 'List ID of citations', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link']
    list_citations = [list_header]
    
    refTable = csv_tools.read_csv_table(listReferences)
    # Note: header of refTable is ['ID', 'Number of references', 'Number of references outside selected database', 'Number of self-cited references', 'List ID of references', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link']
    number_of_citations = [0]*len(refTable)
    id_of_citing_papers = [[] for _ in range(len(refTable))] # initialize array of empty lists, each row contains list of papers that cite this one
    # id_of_citing_papers = [[]]*len(refTable) # theoretically this command also creates an array of empty lists, however due to Python management the append/extend for each item affects all others
    
    for row in refTable[1:]:
        paper_id = str(row[0])
        paper_ref = row[4].split(',')
        if not paper_ref == ['']: # there are some references in the list of papers
            for ref in paper_ref:
                number_of_citations[int(ref)] += 1
                id_of_citing_papers[int(ref)].append(paper_id)
    for k in range(1, len(refTable)):
        list_citations.append([k, number_of_citations[k], ','.join(id_of_citing_papers[k])] + refTable[k][5:])
    
    csv_tools.write_table_csv(exportFile, list_citations)
    #print(list_citations)

