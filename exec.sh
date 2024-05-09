#!/bin/bash

# This Shell script runs the whole program in unison.
# It executes relevant scripts and cleans up helper files that are used.

# Some colors that we will use
BIRed='\033[4;91m'      # Bold High Intensity Red
BWhite='\033[1;37m'     # Bold White
BBlue='\033[1;35m'      # Bold Blue
BIGreen='\033[1;92m'    # Bold High Intensity Green

# Callable paths
build_path="./Build/main.py"
cache_path="./Build/__pycache__"

# Setting up MySQL credentials
clear
echo -e "${BBlue}PHASE 1) Authenticating connection..."

# Credentials are located in a dot env file
source .env
mysql -h $RDS_HOST --user=$RDS_USER --password=$RDS_PASS --ssl-ca=$RDS_CA --ssl-mode=VERIFY_IDENTITY -e "source init_db.sql" 2> error.txt

# Catch access denied error
if grep -q "ERROR 1045" error.txt; then
    clear
    rm error.txt
    echo -e "${BIRed}Incorrect credentials. Please try again."
    exit 1
fi

rm error.txt 

# Start of scraper
sleep 1
echo -e "PHASE 2) Running MorningStar...${BWhite}"

# If the python script is stopped manually:
# Delete the created tables in the first phase
# Delete the scraped text files completely

function exitHandle () {
    # Free hard disk and cleanup temporary files
    # This will happen both on error or operation success
    rm -rf Testing   # Debug folder
    rm -rf Output    # Non debug folder
    rm -rf $cache_path   # Library import cache

    # Deletes all progress in the database when something goes wrong
    if [ $? -gt 0 ]
    then
        mysql -h $RDS_HOST --user=$RDS_USER --password=$RDS_PASS --ssl-ca=$RDS_CA --ssl-mode=VERIFY_IDENTITY -e "drop database MorningStarTest" 2>/dev/null
        echo -e "${BIRed}Error: Action aborted."
    fi
    exit 1
}

set -e
trap "exitHandle" EXIT

# Setup execution permissions for main body of scraper and run it
chmod 744 $build_path   # Added execution permistions
$build_path             # Execute build
chmod 644 $build_path   # Reset permissions
sleep 1

# Transfer data from text files to MySQL
echo -e "${BBlue}PHASE 3) Transferring files..."
mysql --local-infile=1 -h $RDS_HOST -P 3306 --user=$RDS_USER --password=$RDS_PASS --ssl-ca=$RDS_CA --ssl-mode=VERIFY_IDENTITY -e "source pop_db.sql" 2>/dev/null
sleep 1

echo -e "${BIGreen}PHASE 4) Process completed."
sleep 1