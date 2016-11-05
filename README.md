# README #

### Author: Harpreet Dhillon, harpreet@uoregon.edu ###

---

### Purpose ###
* This application is for Project 6 of CIS 322 at University of Oregon.
* The purpose was to get an introduction into MongoDB by creating, inserting, and deleting from a database.

### Application Specifics ###
* The main [index](/templates/index.html) displays current memos and memos can also be deleted from there
* The [create](/templates/create.html) page allows for adding new memos into the database by specifying:
  * Date for memo
  * Text for memo

### Running the Application ###
* Test deployment to other environments including Raspberry Pi.  Deployment 
  should work "out of the box" with this command sequence:
  * `git clone <yourGitRepository> <targetDirectory>`
  * `cd <targetDirectory>`
  * `./configure`
  * `make run`
  * (control-C to stop program)
* The default port is 5000, so the webserver should be reachable at http://localhost:5000 , and also through its IP address.
 
### Testing the Application ###
 * There are nosetests for various situations, including dates for: yesterday, today, and tomorrow.
