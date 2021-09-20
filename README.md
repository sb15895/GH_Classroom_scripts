# Introduction

The aim of this script is to extract information and archive student repositories created by GitHub Classrooms software. When this script is run, it will extract the grades using the CSV file which is obtained from GitHub Classroom Assistant or the web interface. 

## Aim
This file should be able to run on the deadline and complete following tasks:
- Extract information from CSV file
- Output learn compatible CSV file with grades and student IDs
- Run a loop over all repositories from student submissions and archive them on deadline. There is also a function to unarchive the repositories. 

## Steps
- Obtain GitHub API token from your settings page
- Download csv file from [Github Classroom page](https://classroom.github.com/classrooms/87207786-edinburgh-teaching-inf2c-cs) 
- Input both of this in [GraphQL_script.py](GraphQL_script.py) and run program

  ```
  ./GraphQL_script.py --token ghp_cgABCDEFGHIJKLMNOPQRSTUVWXYZ cw0-grades-123456789.csv
  ```
