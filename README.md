# GeoSenseAssist-Project

General Website that will hold all of the different features of the project

How to run GeoSense

**step 1:**
dowload mySQL community
https://dev.mysql.com/downloads/installer/

for macOS you can use homebrew to install mySQL: https://brew.sh/ then once its installed run brew install mySQL in your terminal

**step 2:**
accept all default settings in mySQL, create your root username and password 

**step 3:**
Create a new user with credentials given in Github secrets. 

**step 4:**
 go to google ai studio and create gemini api key.

**step 5:**
create .env file, 
create variable called
API_KEY = insert api key here
HOST_NAME = insert hostname found in group chat here
USER_NAME = insert username found in group chat here
USER_PASSWORD = insert password found in group chat here
DATABASE_NAME = insert database name provided in group chat
(NOTE: do not place the variable data in quotations)

**step 6:**
paste api key, hostname, username, password, and database in .env
 
**step 7:**
run database.py

**step 8:**
run main.py

**step 9:**
use the automated URL link that contains your IP address

