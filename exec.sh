#!/bin/bash

# This Shell script runs the whole program in unison.
# It executes relevant scripts and cleans up helper files that are used.

# Callable paths
build_path="./Build/main.py"
cache_path="./Build/__pycache__"

# Setting up MySQL credentials
clear
echo "Please enter your MySQL credentials."
sleep 1

read -p "Username : " username
read -p "Password : " password
echo ""

echo "Attempting to build MySQL database..."
sleep 1

mysql --user=$username --password=$password -e "source tablespawn.sql" 2> error.txt

# Catch access denied error
if grep -q "ERROR 1045" error.txt; then
    clear
    rm error.txt
    echo "Incorrect credentials. Please try again."
    sleep 1
    exit
fi

rm error.txt 

# Start of scraper
clear
echo "Running MorningStar."
echo ""
sleep 1

# Setup execution permissions for main body of scraper and run it
chmod 744 $build_path   # Added execution permistions
$build_path             # Execute build
chmod 644 $build_path   # Reset permissions
sleep 2

# Transfer data from text files to MySQL
clear
echo "Transferring files."
mysql --user=$username --password=$password -e "source transfertext.sql" 2>/dev/null
sleep 1

# Free hard disk and cleanup temporary files
rm -rf Testing       # Debug folder
rm -rf Output        # Non debug folder
rm -rf $cache_path   # Library import cache

clear
echo "MorningStar processes completed."
sleep 1