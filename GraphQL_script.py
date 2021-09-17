# graphQL archive code from https://gist.github.com/lotharschulz/9d80ecac73806981a6adc7e5ab2eb9a3
# headers = {"Authorization": "Bearer <your Github token>"} 
# input filename of CSV file downloaded from GH classrooms in variable input_file
# owner is name of GH organisation
# github repos obtained from import_repo_list of input_file

import requests
import pandas as pd 
import sys
from GraphQL_utils import *

headers = {"Authorization": "Bearer <your Github token>"} 
input_file = '<InputCSVfile>'
# if you want to use the safer option, you can pass your GH token in the command line or in a bash file. 
# token = 'Bearer '+sys.argv[1] #command line passing of bearer token
# headers = {'Authorization' : token}
# input_file = sys.argv[2]

owner = 'edinburgh-teaching'

repo_list = [0]*500
repo_list = import_repo_list(input_file) #function to import repo list from file
print(repo_list)

grades_result(input_file) # function to extract learn compatible CSV file from GH classroom CSV file

for x in range(len(repo_list)):
    
    archive(get_repoID(owner,repo_list[x])) # function to archive repo 
    unarchive(get_repoID(owner,repo_list[x])) # function to unarchive repo 

