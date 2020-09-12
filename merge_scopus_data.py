# Script to extract papers from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 merge_scopus_data.py
# Default output is file all_database.csv
# Other way: python3 merge_scopus_data.py data_folder output_file.csv

import os
import sys
import csv_tools

    
## Main operation, when calling: python merge_scopus_data.py data_folder output_file.csv
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'all_database.csv'

    #merge_scopus_data(dataFolder, exportFile)
    merged_table = []
    processed_papers = []

    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                print('Processing file ' + csvFile)
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Title' in headerTable:
                    title_index = headerTable.index('Title')
                    for row in table[1:]:
                        if not row[title_index] in processed_papers:
                            processed_papers.append(row[title_index])
                            merged_table.append(row)

    # This command should be executed after all the papers were collected
    merged_table.sort(key=lambda x:x[title_index],reverse=False) # sort by title, assume all data files have the same header
    merged_table.insert(0, headerTable)
    csv_tools.write_table_csv(exportFile, merged_table)
    #print(list_papers)
    print('Merging finished. Result is written to file ' + exportFile)

    