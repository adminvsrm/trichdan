# Script to extract references from Scopus exported data
# Dang Doan, 2020-09
# Usage: put csv files exported from Scopus to folder scopus_data, then run command: python3 get_references.py
# Output is file list_references.csv
# Other way: python3 get_references.py data_folder output_file.csv list_of_papers.csv

import os
import sys
import csv_tools
import re

def parse_references(ref_text):
    # Parse the Authors with affiliations for each article
    # Example text: Aziz, A., Jamshed, W., Ali, Y., Shams, O.S.P.S.P., Heat transfer and entropy analysis of Maxwell hybrid nanofluid including effects of inclined magnetic field, Joule heating and thermal radiation (2019) Discr. Contin. Dyn. Syst. Ser. S, 2019, p. 1937; Minea, A.A., Moldoveanu, M.G., Overview of hybrid nanofluids development and benefits (2018) Journal of Engineering Thermophysics, 27 (4), pp. 507-514; Chamkha, A.J., Dogonchi, A.S., Ganji, D.D., Magneto-hydrodynamic flow and heat transfer of a hybrid nanofluid in a rotating system among two surfaces in the presence of thermal radiation and joule heating (2019) AIP Advances, 9 (2), p. 025103; Bui-Thanh, T., Damodaran, M., Willcox, K., Proper orthogonal decomposition extensions for parametric applications in transonic aerodynamics AIAA, 15th Computational Fluid Dynamics Conference, (Orlando, FL); Global emission. Analysis: coronavirus set to cause largest ever annual fall in CO2 emissions https://www.carbonbrief.org/analysis-coronavirus-set-to-cause-largest-ever-annual-fall-in-co2-emissions, Available at: (Accessed 9 April 2020)
    year_pattern = re.compile("^(.+)(\(\d\d\d\d\))(.*)")
    cap_pattern = re.compile("^(.+)(\ [A-Z]{2,}\,)(.*)")
    list_ref = ref_text.split(';')
    list_parsed = []
    list_authors_fullname = []
    list_titles = []
    for ref in list_ref:
        first_compare = year_pattern.match(ref)
        if not first_compare==None:
            authors_and_title = ref[first_compare.span(1)[0]:first_compare.span(1)[1]]
        else: # year missing
            second_compare = cap_pattern.match(ref)
            if not second_compare==None:
                authors_and_title = ref[second_compare.span(1)[0]:second_compare.span(1)[1]]
            else: # pattern of reference could not be recognized, skip it
                continue
        split_pos = authors_and_title.rfind('.,')
        authors_text = authors_and_title[:split_pos+1]
        title = authors_and_title[split_pos+2:].strip()
        list_titles.append(title)
        authors = authors_text.split(',')
        authors_fullname = []
        for k in range(len(authors)//2):
            lastname = authors[2*k]
            firstname = authors[2*k+1]
            authors_fullname.append(lastname.strip() + ' ' + firstname.strip())
        list_authors_fullname.append(authors_fullname)
    
    return list_authors_fullname, list_titles


## Main operation, when calling: python get_authors.py data_folder
if __name__ == "__main__":
    if len(sys.argv)>1:
        dataFolder = str(sys.argv[1])
    else:
        dataFolder = 'scopus_data'
    if len(sys.argv)>2:
        exportFile = str(sys.argv[2])
    else:
        exportFile = 'list_references.csv'
    if len(sys.argv)>3:
        listPaper = str(sys.argv[3])
    else:
        listPaper = 'list_papers.csv'

    #get_papers(dataFolder, exportFile)
    list_header = ['ID', 'Number of references', 'Number of references outside selected database', 'Number of self-cited references', 'List ID of references', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link']
    list_references = [list_header]
    
    paperTable = csv_tools.read_csv_table(listPaper)
    # Note: header of paperTable is ['ID', 'Title', 'Authors', 'Source title', 'Publisher', 'Year', 'Link']
    paperTable_transpose = csv_tools.transpose_table(paperTable)
    for k in range(1,len(paperTable_transpose[2])):
        authors_split = paperTable_transpose[2][k].split(',')
        paperTable_transpose[2][k] = [item.strip() for item in authors_split]
    
    for dirpath, dirs, files in os.walk(dataFolder):
        for filename in files:
            if filename[-4:].upper() == '.CSV':
                csvFile = os.path.join(dirpath,filename)
                # For each CSV file
                table = csv_tools.read_csv_table(csvFile)
                headerTable = table[0]
                if 'Authors' in headerTable and 'Title' in headerTable and 'References' in headerTable:
                    title_index = headerTable.index('Title')
                    author_index = headerTable.index('Authors')
                    ref_index = headerTable.index('References')
                    access_index = [title_index, author_index, ref_index]
                    for row in table[1:]:
                        if row[title_index] in paperTable_transpose[1]: # title appears in the database (should be true)
                            id_in_paperTable = paperTable_transpose[1].index(row[title_index])
                            if id_in_paperTable not in [row[0] for row in list_references]: # references of this paper was not yet processed
                                ref_authors, ref_titles = parse_references(row[ref_index])
                            
                                no_ref = len(ref_titles)
                                no_ref_ext = 0
                                no_ref_self = 0
                                list_ref_IDs = []
                                for kk in range(len(ref_titles)):
                                    paper_title = ref_titles[kk]
                                    paper_authors = ref_authors[kk]                                
                                    if not paper_title in paperTable_transpose[1]:
                                        no_ref_ext += 1
                                    else: # reference is in the paper table
                                        ref_id_in_paperTable = paperTable_transpose[1].index(paper_title)
                                        list_ref_IDs.append(str(ref_id_in_paperTable))
                                        self_cite_flag = False
                                        for single_author in paper_authors:
                                            if single_author in paperTable_transpose[2][ref_id_in_paperTable]:
                                                self_cite_flag = True
                                        if self_cite_flag == True:
                                            no_ref_self += 1
                                list_ref_IDs_string = ','.join(list_ref_IDs)
                                ref_detail_row = [id_in_paperTable, no_ref, no_ref_ext, no_ref_self, list_ref_IDs_string] + paperTable[id_in_paperTable][1:]
                                list_references.append(ref_detail_row)
                            
                                
    # This command should be executed after all the references were collected
    del list_references[0] # remove header line before sorting
    list_references.sort(key=lambda x:x[0],reverse=False) # sort by ID
    list_references.insert(0, list_header)
    csv_tools.write_table_csv(exportFile, list_references)
    #print(list_references)

