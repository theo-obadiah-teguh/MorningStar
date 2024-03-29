/* 
This script sets up our new database called MorningStar.
It also includes the necessary Data Definition Language (DDL).
It then transfers parsed data from .txt to our newly setup database.
*/

-- Initialize the new database
CREATE DATABASE MorningStarTest;

-- Access that new database
USE MorningStarTest;

-- SQL Data Definition Language (DDL) for the PortfolioSummary entity
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

-- SQL Data Definition Language (DDL) for the HoldingDetail entity
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