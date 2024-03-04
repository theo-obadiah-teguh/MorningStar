

-- CREATE DATABASE Morningstar

USE Morningstar

-- Create necessary tables

CREATE TABLE IF NOT EXISTS PortfolioSummaryX (
Filename VARCHAR(30),
Portfolio_ORDINAL INT,
Fund_Name VARCHAR(40),
ShareClassId VARCHAR(20),
_Date CHAR(10),
_CurrencyId VARCHAR(20),
PortfolioSummary_ORDINAL INT,
NumberOfHoldingShort INT,      
NumberOfStockHoldingShort INT,
NumberOfBondHoldingShort INT, 
TotalMarketValueShort INT, 
NumberOfHoldingLong INT, 
NumberOfStockHoldingLong INT, 
NumberOfBondHoldingLong INT, 
TotalMarketValueLong INT
);

CREATE TABLE IF NOT EXISTS HoldingDetailX (
Filename VARCHAR(30),
Portfolio_ORDINAL INT,
Fund_Name VARCHAR(40),
ShareClassId VARCHAR(20),
_Date CHAR(10),
_CurrencyId VARCHAR(20),
PortfolioSummary_ORDINAL INT,
Holding_Ordinal INT,
_DetailHoldingTypeId VARCHAR(20),
_ExternalId VARCHAR(20),
_Id VARCHAR(20),
Country_Id VARCHAR(20),
Country VARCHAR(20),
CUSIP VARCHAR(20),
SEDOL VARCHAR(20),
ISIN VARCHAR(20),
Ticker VARCHAR(20),
Currency VARCHAR(20),
Currency_Id VARCHAR(20),
SecurityName VARCHAR(20),
Weighting VARCHAR(20),
NumberOfShare INT,
SharePercentage VARCHAR(20),
MarketValue INT,
CostBasis VARCHAR(20),
ShareChange INT,
Sector VARCHAR(20),
MaturityDate VARCHAR(20),
Coupon VARCHAR(20),
CreditQuality VARCHAR(20),
Duration VARCHAR(20),
IndustryId VARCHAR(20),
PaymentType VARCHAR(20),
Rule144AEligible VARCHAR(20),
AltMinTaxEligible VARCHAR(20),
FirstBoughtDate VARCHAR(20),
LessThanOneYearBond VARCHAR(20)
);

-- Upload all data from PSX and HDX

SET GLOBAL local_infile = TRUE ;

LOAD DATA LOCAL INFILE '/Users/theoobadiahteguh/Desktop/Morningstar/Output/TextFiles/PSX.txt'
INTO TABLE PortfolioSummaryX 
FIELDS TERMINATED BY ';'  
LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '/Users/theoobadiahteguh/Desktop/Morningstar/Output/TextFiles/HDX.txt'
INTO TABLE HoldingDetailX 
FIELDS TERMINATED BY ';'  
LINES TERMINATED BY '\n';

-- Import ComparisonData with a Python Jupyter Notebook Script and update the columns and datatypes

ALTER TABLE ComparisonData
	CHANGE issue_id Issue_Id INT,
	CHANGE crsp_cl_grp crsp_cl_grp INT,
	CHANGE fundid Fund_Id VARCHAR(20),
	CHANGE quarter _Quarter INT,
	CHANGE month _Month INT,
	CHANGE cusip CUSIP VARCHAR(20),
	CHANGE mktval MarketValue BIGINT,
	CHANGE shares NumberOfShare BIGINT,
	CHANGE portdate _Date CHAR(19),
	CHANGE sign Sign INT,
	CHANGE short_long_ratio Short_Long_Ratio FLOAT(64,10),
	CHANGE totmktval_long TotalMarketValueLong BIGINT,
	CHANGE totmktval TotalMarketValue BIGINT,
	CHANGE bond_type BondType CHAR(4),
	CHANGE corp_bond CorpBond INT,
	CHANGE wght Weighting FLOAT(64,10),
	CHANGE wght_corp Weighting_Corp FLOAT(64,10);

-- Change Date column datatype after all tables are ready

UPDATE PortfolioSummaryX 
SET _Date = STR_TO_DATE(_Date, '%Y-%m-%d');

UPDATE HoldingDetailX 
SET _Date = STR_TO_DATE(_Date, '%Y-%m-%d');

UPDATE ComparisonData
SET _Date = DATE_FORMAT(_Date, '%Y-%m-%d');

-- Continue to filtration script
