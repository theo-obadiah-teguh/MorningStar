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
