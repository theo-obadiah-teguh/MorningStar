/* 
This script parses data from our text files and inputs it to our database.
*/

-- Set permission load data
SET GLOBAL local_infile = TRUE;
USE MorningStarTest;

-- Moves the contents of PSX to the PorfolioSummaryX table
LOAD DATA LOCAL INFILE './Testing/TextFiles/PSX.txt'
INTO TABLE PortfolioSummaryX 
FIELDS TERMINATED BY ';'  
LINES TERMINATED BY '\n';

-- Moves the contents of HDX to the HoldingDetailsX table
LOAD DATA LOCAL INFILE './Testing/TextFiles/HDX.txt'
INTO TABLE HoldingDetailX 
FIELDS TERMINATED BY ';'  
LINES TERMINATED BY '\n';

-- Change _Date columns' datatype after all tables are ready
UPDATE PortfolioSummaryX 
SET _Date = STR_TO_DATE(_Date, '%Y-%m-%d');

UPDATE HoldingDetailX 
SET _Date = STR_TO_DATE(_Date, '%Y-%m-%d');