# COMP3005 Queries Code (ver 1.2)
> The following queries.py file is the template code for COMP3005 Database Project 1, which will be used for the autograder.
>
> **This README is an _important_ guide to effectively using this repository and finishing this project.**

### Updates (04/13/2024)
```Ver 1.11 -> Ver 1.2
- Changed dbexport.sql reading bug where directories with spaces caused crashes.
- Fixed connection/cursor linkage, solving the overarching multipled-values bug.
- Added additional information on how to change postgres user password.
- Added dump so that when dbexport.sql is dumping, no text is provided (output is sent to /dev/null).
```
## Starter Code:
- _queries.py_
  - This will be the file you will write your queries in **AND** submit.
- _dbexport.sql_
  - This is an **example** of an exported database. This can be used for testing, for both you and myself.

## Modules and Dependencies:
This project, and in turn the autograder and starter code, uses psycopg3 on a v22.04 Ubuntu Linux environment. 
- [psycopg3 Installation and Documentation](https://www.psycopg.org/psycopg3/docs/)
- [Carleton University VM Downloads](https://carleton.ca/scs/tech-support/virtual-machines/)
- [PostgreSQL](https://ubuntu.com/server/docs/databases-postgresql)
- [pgAdmin4](https://www.pgadmin.org/download/pgadmin-4-apt/) (This is ideal to create and test your databases).

## Task:
As per the project guidelines,
>"Design a database that stores a soccer events dataset spanning multiple competitions and seasons. The provided
dataset is in JSON format and can be downloaded from https://github.com/statsbomb/open-data/tree/0067cae166a56aa80b2ef18f61e16158d6a7359a1. The documentation of the dataset is also available in the
above URL. After designing the database, you need to import the data from the JSON files into your database."

Once your database has been designed, you are then tasked to export this database into an .sql file named "dbexport" - this can be accomplished using [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html).

Given that the previous two steps are accomplished, your task is to now ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

This given task must be completed on an Ubuntu Linux environment, see above.

## Testing:
The _queries.py_ file and your exported _dbexport.sql_ file should be within the same directory.

The _queries.py_ file includes the following code snippet,
```
root_database_name = "project_database"
query_database_name = "query_database"
db_username = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '5432'
```
To briefly explain, these variables are used to connect to the root database named "project_database" and your query execution database named "query_database."
The code's process for each query is to create a database named "query_database", import your dbexport.sql file into this database, execute the query, and then drop the database (to avoid any alterations so results are not affected down the line).
The reasoning for two databases is because the connection cannot drop a database it is currently connected to, hence the two databases - one for a root connection and one for query execution.

You _may_ change these values to test on your end, **but under _no circumstance in the final deliverable should these initial values be different_.**

Expected Output:
> While testing, your outputare your query times.
> **INC** simply means incomplete.

## Warning:
As the autograder is also connecting to your databases, to reiterate, any change to the initial values of the connection variables will result in your code submission becoming _void_. You may change these values for your own testing purposes, (e.g, you have a different password), but do so at your discretion.
  - What else will _VOID_ your submission?
    - Any _additional_ submissions in your repository.
    - _Other_ print statements.
    - Other alterations to code other than the query executions (please view ACADEMIC INTEGRITY below).
      
## Final Deliverable:
Your source code file(s) that maps and loads the existing JSON dataset from the JSON files into your database. This code must be stored in a directory named "json_loader".
Therefore, in your submission repository, you are _only_ submitting the script "queries.py", *your* dbexport.sql, ".gitattributes" when you import the dbexport.sql as an LFS, and the "json_loader" directory.
Any additional submissions will ***void*** the entire ***code submission.***

### How to Submit Large Files
GitHub has a restriction to submission size - if any file exceeds 100.00 MB it simply cannot be added to your repository - so for this case, your dbexport.sql. Luckily, you may use Git LFS to your advantage.
Git LFS (Large File Storage) allows the submission of these large files by using reference pointers to get this data - this will be beneficial for both you and the grader.

**Steps:**
- Install _git_ and _git lfs_ in your Linux terminal, use the following commands to install **both**.
  - ```sudo apt-get install git-all```
  - ```curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash```
  - ```sudo apt-get install git-lfs```
  
  Next, you will set up your GitHub username and email,
  - ```git config --global user.name "Your Name"```
  - ```git config --global user.email "Your Email"```
- Have a directory based on your submission, in other words, have a folder on your system containing all files you will have in your repository submission. This is both easier and organized for you, but also allows you to do the git commands without the worry of affected anything outside of it.
  
![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/6424f73f-28fb-4f6c-8b34-44aa712c8617)

- Open the terminal with this directory, and then write the following line, this will create a _HIDDEN_ .git folder in your folder:
  - ```git init```
  
![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/8df92eec-ab31-4c89-b5a5-b7ff87cf5041)

- Then, write the following line to track your dbexport into a smaller reference file:
  - ```git lfs track "*.sql"```
  
![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/5b49a789-20be-4b3c-9be7-654577a3fad4)

- Once this is done, you can then do the following lines of code in your terminal.
  - ```git branch -M main```
  - ```git remote add origin "your submission .git link"```
  - ```git add "your files that you will add to your submission"```
    - Example: ```git add queries.py```
- Once you add your files, you can check your additions to the commit by doing ```git status```
  - BEFORE
    
  ![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/847a64b7-6ff3-44ae-9f43-a1cc19b26bc6)
  - AFTER ADDING
    
  ![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/03af84d0-6ef3-4e61-aba7-1b23e3f1734e)
- Then, you can commit using ```git commit -m "Commit Message"```
- And then finally, you can push to your repository, ```git push -u origin main```
- The terminal would then prompt you for your GitHub username and password, however, as of August 13th, 2021, GitHub has removed account password authentication for terminal pushes. Therefore, please use this following [article](https://dev.to/shafia/support-for-password-authentication-was-removed-please-use-a-personal-access-token-instead-4nbk) to set up your own authentication key.
- It will loop and continously ask for your username and password based on how many files you are pushing!

- Your following submission should then look like the following:
![image](https://github.com/gabrielmartell/COMP3005-Project-Template/assets/120336080/19e76627-a700-4886-b294-afb95af25999)

- If your database is less than 100MB and you didn't track it, your output would be like this minus the .gitattributes.
## Bugs and Questions:
If you run into any fatal errors or bugs, please consult the [closed issues](https://github.com/gabrielmartell/COMP3005-Project-Template/issues?q=is%3Aissue+is%3Aclosed) first as it might have already been solved.
If it hasn't been solved, and/or you also have questions, please feel free to create an [open issue!](https://github.com/gabrielmartell/COMP3305-Project-Template/issues). If need be, you can also shoot me an email at gabemartell@cmail.carleton.ca - although I would respond quicker to the GitHub issues.

# CARLETON ACADEMIC INTEGRITY
Any alterations to the code, such as modifying the time, will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean.
To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 
