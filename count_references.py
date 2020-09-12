# Script to count references - citations from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, run get_papers.py and get_references.py, put list of selected authors in the file input_net_authors.txt, then run command: python3 count_references.py
# Output is file references_net.csv
# Other way: python3 count_references.py data_folder output_file.csv list_of_references.csv input_net_authors.txt

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
        exportFile = 'references_net.csv'
    if len(sys.argv)>3:
        listReferences = str(sys.argv[3])
    else:
        listReferences = 'list_references.csv'
    if len(sys.argv)>4:
        listNetAuthors = str(sys.argv[3])
    else:
        listNetAuthors = 'input_net_authors.txt'


    #count_references(dataFolder, exportFile, listReferences, listNetAuthors)
    list_header = ['ID', 'Author', 'Number of papers', 'Number of papers citing (one of) network authors', 'Number of papers receiving citations from network authors', 'Number of referring papers co-authored by network authors', 'Number of citing papers co-authored by network authors', 'Total number of references in author\' papers', 'Number of references to network authors (self cite + ring cite)', 'Number of citations from network authors']
    list_stats = [list_header]
    with open(listNetAuthors, "rt") as textfile:
        author_lines = textfile.readlines()
    filtered_authors = [x.strip() for x in author_lines if x.strip()]
    
    no_papers = [0]*len(filtered_authors)
    no_papers_citing_net = [0]*len(filtered_authors)
    no_papers_cited_by_net = [0]*len(filtered_authors)
    no_refs_to_net = [0]*len(filtered_authors)
    no_citations_from_net = [0]*len(filtered_authors)
    no_total_refs = [0]*len(filtered_authors)
    no_times_references_to_net = [0]*len(filtered_authors)
    no_times_citations_from_net = [0]*len(filtered_authors)
    temp_list_papers_with_references_to_net = [[] for _ in range(len(filtered_authors))]
    temp_list_papers_with_citations_from_net = [[] for _ in range(len(filtered_authors))]
    temp_list_references_to_net = [[] for _ in range(len(filtered_authors))]
    temp_list_citations_from_net = [[] for _ in range(len(filtered_authors))]
    temp_list_ref_pairs_within_net = [[] for _ in range(len(filtered_authors))]
    temp_list_cite_pairs_within_net = [[] for _ in range(len(filtered_authors))]
    
    matrix_references = [ [0 for _ in range(len(filtered_authors))] for _ in range(len(filtered_authors)) ] # each cell is number of references: author in row cite author in column
    #matrix_citations = [ [0 for _ in range(len(filtered_authors))] for _ in range(len(filtered_authors)) ] # each cell is number of citations: author in row cited by author in column
    
    refTable = csv_tools.read_csv_table(listReferences)
    # Note: header of refTable is ['ID', 'Number of references', 'Number of references outside selected database', 'Number of self-cited references', 'List ID of references', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link', 'Rating', columns of references by rating]
    
    rating_list = list(dict.fromkeys([row[11] for row in refTable[1:]]))
    matrix_cite_with_rating = [ [0 for _ in range(len(rating_list))] for _ in range(len(filtered_authors)) ]
    
    # First, split author text into list of authors, and split reference text into list of references ID
    for row in refTable[1:]:
        temp = row[6].split(',')
        row[6] = [x.strip() for x in temp if x.strip()]
        temp2 = row[4].split(',')
        row[4] = temp2 if not temp2==[''] else []
    
    # Then scan the table of references to do counting
    for row in refTable[1:]:
        paper_id = str(row[0])
        #print('Processing paper: ', paper_id)
        # Count citations by rating
        for ref_id in row[4]:
            #print(row)
            #print(ref_id)
            authors_of_ref = refTable[int(ref_id)][6]
            for ref_author in authors_of_ref:
                if ref_author in filtered_authors: # citation for one author of the network
                    citation_rating = refTable[int(ref_id)][11]
                    matrix_cite_with_rating[filtered_authors.index(ref_author)][rating_list.index(citation_rating)] += 1
        
        for person in row[6]:
            if person in filtered_authors:
                no_papers[filtered_authors.index(person)] += 1
                no_total_refs[filtered_authors.index(person)] += int(row[1])
                #print(row[4])
                for ref_id in row[4]: # row[4] is List ID of references
                    #print(' ref_id', ref_id)
                    authors_of_ref = refTable[int(ref_id)][6] # note that ID corresponds to the row number of the paper in refTable, so we access directly row number=ref_id instead of searching for ref_id in first column of refTable
                    for ref_author in authors_of_ref:
                        if ref_author in filtered_authors: # reference is co-authored by one author of the network
                            if not paper_id in temp_list_papers_with_references_to_net[filtered_authors.index(person)]:
                                temp_list_papers_with_references_to_net[filtered_authors.index(person)].append(paper_id)
                                no_papers_citing_net[filtered_authors.index(person)] += 1
                            
                            if not ref_id in temp_list_papers_with_citations_from_net[filtered_authors.index(ref_author)]:
                                temp_list_papers_with_citations_from_net[filtered_authors.index(ref_author)].append(ref_id)
                                no_papers_cited_by_net[filtered_authors.index(ref_author)] += 1
                            
                            if not ref_id in temp_list_references_to_net[filtered_authors.index(person)]:
                                temp_list_references_to_net[filtered_authors.index(person)].append(ref_id)
                                no_refs_to_net[filtered_authors.index(person)] += 1

                            if not paper_id in temp_list_citations_from_net[filtered_authors.index(ref_author)]:
                                temp_list_citations_from_net[filtered_authors.index(ref_author)].append(paper_id)
                                no_citations_from_net[filtered_authors.index(ref_author)] += 1
                            
                            if not (paper_id, ref_id) in temp_list_ref_pairs_within_net[filtered_authors.index(person)]:
                                temp_list_ref_pairs_within_net[filtered_authors.index(person)].append((paper_id, ref_id))
                                no_times_references_to_net[filtered_authors.index(person)] += 1
                            
                            if not (paper_id, ref_id) in temp_list_cite_pairs_within_net[filtered_authors.index(ref_author)]:
                                temp_list_cite_pairs_within_net[filtered_authors.index(ref_author)].append((paper_id, ref_id))
                                no_times_citations_from_net[filtered_authors.index(ref_author)] += 1
                            
                            matrix_references[filtered_authors.index(person)][filtered_authors.index(ref_author)] += 1
                            #matrix_citations[filtered_authors.index(ref_author)][filtered_authors.index(person)] += 1 # just the transpose of matrix_references
                            
    
    for k in range(len(filtered_authors)):
        list_stats.append([k+1, filtered_authors[k], no_papers[k], no_papers_citing_net[k], no_papers_cited_by_net[k], no_refs_to_net[k], no_citations_from_net[k], no_total_refs[k], no_times_references_to_net[k], no_times_citations_from_net[k]] + matrix_cite_with_rating[k] + matrix_references[k])
    
    # Extend the header
    for rating in rating_list:
        list_stats[0].append('Citation rating: ' + rating)
    for author in filtered_authors:
        list_stats[0].append(author + ' (cited by author in row)')
    
    csv_tools.write_table_csv(exportFile, list_stats)
    #print(list_stats)
    print('Analysis finished. Result is written to file ' + exportFile)
    