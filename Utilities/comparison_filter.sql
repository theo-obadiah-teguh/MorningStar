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
UPDATE ComparisonData
SET _Date = DATE_FORMAT(_Date, '%Y-%m-%d');

-- Some stuff
CREATE TABLE IF NOT EXISTS HDX_Comparison (
Fund_Name VARCHAR(40),
_Date DATE,
CUSIP VARCHAR(20),
NumberOfShare BIGINT,
Ticker VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Checker_Comparison (
crsp_cl_grp VARCHAR(20),
_Date DATE,
CUSIP VARCHAR(20),
NumberOfShare BIGINT
);

INSERT INTO HDX_Comparison (Fund_Name, _Date, CUSIP, NumberOfShare, Ticker)
SELECT Fund_Name, _Date, CUSIP, NumberOfShare, Ticker FROM HoldingDetailX WHERE _Date < '20200930';

INSERT INTO Checker_Comparison (crsp_cl_grp, _Date, CUSIP, NumberOfShare)
SELECT crsp_cl_grp, _Date, CUSIP, NumberOfShare FROM ComparisonData;

SELECT * FROM HDX_Comparison hc 
SELECT * FROM Checker_Comparison
