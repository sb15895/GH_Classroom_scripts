import requests
import pandas as pd 
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np

data = "@archiveRepository.graphql"
url = "https://api.github.com/graphql"

# A simple function to use requests.post to make the API call
def run_query(query, variables, headers): 
    request = requests.post(url, json={'query': query, 'variables': variables, 'data': data}, headers=headers)
    print(request.text)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# function to return repo id of specified github repo
def get_repoID(owner, reponame):

    # query object repo_id, interacts with GitHub API to get repo ID

    repoid = """
    query FindRepoID($owner: String!, $reponame: String!)  {
        repository(owner:$owner, name:$reponame){
            id,
            isArchived,
        }
    }"""

    variables_repoid = {
        "owner" : owner, 
        "reponame" : reponame
    }

    repo_id = run_query(repoid,variables_repoid)
    repoID = repo_id["data"]["repository"]["id"] 
    return(repoID) 

# function to archive repo from repoID
def archive(repoID):

    archive_repo = '''
    mutation ArchiveRepository ($mutationID: String!, $repoID: String!) 
    {
        archiveRepository(input:{clientMutationId:$mutationID, repositoryId:$repoID}) 
        {
            repository
            {
                isArchived,
                description,
            }
        }
    }'''

    variables_archiverepo = {
        "mutationID" : "true", 
        "repoID" : repoID
    }

    result = run_query(archive_repo, variables_archiverepo) # Execute the query

# function to unarchive repo 
def unarchive(repoID):

    unarchive_repo = '''
    mutation UnArchiveRepository ($mutationID: String!, $repoID: String!) 
    {
        unarchiveRepository(input:{clientMutationId:$mutationID, repositoryId:$repoID}) 
        {
            repository
            {
                isArchived,
                description,
            }
        }
    }'''

    variables_unarchiverepo = {
        "mutationID" : "true", 
        "repoID" : repoID
    }

    result = run_query(unarchive_repo, variables_unarchiverepo) # Execute the query

# function to retrieve student number from file 
def studentno_retrieve(owner, reponame):
     
    query = """
    query($owner: String!, $name: String!)
    {   repository(owner: $owner, name: $name)
        {   
            name
            object(expression: "main:src/file")
            {
                ... on Tree
                {
                    entries 
                    {
                        # name
                        # type
                        object 
                        {
                            ... on Blob 
                            {
                            # byteSize
                            text
                            }
                        }
                    }
                }
            }
        }
    }"""

    variables = {
        "owner" : owner, 
        "name" : reponame
    }

    result = run_query(query, variables) # Execute the query
    s_no = result["data"]["repository"]["object"]['entries'][0]['object']['text'] 
    repo_name = result["data"]["repository"]["name"]

    st_num = pd.DataFrame(data, columns=['Student Number', 'Repository Name'])
    st_num.to_csv('log.csv', index = False)
    return(s_no)

# function to obtain grades from repo and get learn compatible CSV file
def grades_result(datfile):

    export_file = "GH_learn_export.csv"

    grades = [-1]*500  #so it doesnt get confused with scores. 
    username = [-1]*500
    roster = [-1]*500

    # Columns "assignment_name","assignment_url","starter_code_url","github_username","roster_identifier","student_repository_name","student_repository_url","submission_timestamp","points_awarded","points_available"
    mydata = pd.read_csv(datfile)

    grades = np.array(mydata.points_awarded)
    usernames = np.array(mydata.github_username)
    # roster = mydata.roster_identifiers 
    data = {'Grades' : grades,'Usernames' : usernames}

    # Learn compatible CSV file
    export_data = pd.DataFrame(data, columns=['Grades','Usernames'])
    export_data.to_csv(export_file, index = False, header = True)

def import_repo_list(datfile):

    repo_names = [0]*500  #so it doesnt get confused with scores. 
    # Columns "assignment_name","assignment_url","starter_code_url","github_username","roster_identifier","student_repository_name","student_repository_url","submission_timestamp","points_awarded","points_available"
    mydata = pd.read_csv(datfile)
    repo_names = np.array(mydata.student_repository_name) # export repo names list 
    return(repo_names)

# def branch_protection():

#      https://api.github.com/repos/$REPOORG/$REPO/branches/main/protection -d '{"required_status_checks": null,"enforce_admins": null,"required_pull_request_reviews" : {"dismissal_restrictions": {},"dismiss_stale_reviews": false,"require_code_owner_reviews": true,"required_approving_review_count": 1},"restrictions":null}'

#     query = """
#     query($owner: String!, $name: String!)
#     {   repository(owner: $owner, name: $name)
#         {   
#             name
#             object(expression: "main:src/file")
#             {
#                 ... on Tree
#                 {
#                     entries 
#                     {
#                         # name
#                         # type
#                         object 
#                         {
#                             ... on Blob 
#                             {
#                             # byteSize
#                             text
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     }"""

#     variables = {
#         "owner" : owner, 
#         "name" : reponame
#     }