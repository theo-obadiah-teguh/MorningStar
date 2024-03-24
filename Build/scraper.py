# This script is the main body of the XML scraper.
# It will go through a given dataset.

# The first is "PSX.txt" which is a cleaned file for portfolio summaries.
# The second is "HDX.txt" which is a cleaned file for holding details.

# All the datasets will be aggregated in these two files.
# These two files will be placed in a temporary folder called "TextFiles".
# These two outputs will later be parsed into an SQL database.

import os

def create_txtfile (iterable, Filename, debug) :
    
    if debug : 
        txtfile_path = './Testing/TextFiles'
    else : 
        txtfile_path = './Output/TextFiles'

    # Check if the output folder has been created
    isExist = os.path.exists(txtfile_path)

    # Creates a an output folder if needed
    if not isExist: 
        os.makedirs(txtfile_path)
    
    psx_handle = open(f"{txtfile_path}/PSX.txt", 'a')
    hdx_handle = open(f"{txtfile_path}/HDX.txt", 'a')
    
    del txtfile_path
    
    Section = None
    
    # The items needed for both data frames
    Portfolio_ORDINAL         = 0
    Fund_Name                 = None
    ShareClassId              = None # Use Investment Vehicle ID
    Date                      = None
    _CurrencyId               = None
    PortfolioSummary_ORDINAL  = 0
    #PreviousPortfolioDate    = None
    #NetExpenseRatio          = 0
    
    # All the items needed specifically for PortfolioSummaryX
    
    psx_cache = []
    
    NumberOfHoldingShort      = '0'
    NumberOfStockHoldingShort = '0'
    NumberOfBondHoldingShort  = '0'
    TotalMarketValueShort     = '0'
    NumberOfHoldingLong       = '0'
    NumberOfStockHoldingLong  = '0'
    NumberOfBondHoldingLong   = '0'
    TotalMarketValueLong      = '0'
    
    # All the items needed specifically for HoldingDetailX
    
    hdx_cache = []
    
    # HoldingOrdinal is assigned when entering a section
    _DetailHoldingTypeId             = None
    #_StorageId                      = None
    _ExternalId                      = None
    _Id                              = None
    #ExternalName                    = None
    Country_Id                       = None
    Country                          = None
    CUSIP                            = None
    SEDOL                            = None
    ISIN                             = None
    Ticker                           = None
    Currency                         = None
    Currency_Id                      = None
    SecurityName                     = None
    #LocalName                       = None
    Weighting                        = None
    NumberOfShare                    = '0'
    SharePercentage                  = None
    #NumberOfJointlyOwnedShare       = None
    MarketValue                      = '0'
    CostBasis                        = None
    ShareChange                      = '0'
    Sector                           = None
    MaturityDate                     = None
    #AccruedInterest                 = None
    Coupon                           = None
    CreditQuality                    = None
    Duration                         = None
    IndustryId                       = None
    #GlobalIndustryId                = None
    #GlobalSector                    = None
    #GICSIndustryId                  = None
    #LocalCurrencyCode               = None
    #LocalMarketValue                = None
    #ZAFAssetType                    = None
    PaymentType                      = None
    Rule144AEligible                 = None
    AltMinTaxEligible                = None
    #BloombergTicker                 = None
    #ISOExchangeID                   = None
    #ContractSize                    = None
    #SecondarySectorId               = None
    #CompanyId                       = None # Operation
    FirstBoughtDate                  = None
    #MexicanTipoValor                = None
    #MexicanSerie                    = None
    #MexicanEmisora                  = None
    #UnderlyingSecId                 = None # UnderlyingFundId in InvestmentVehicle/SubAccount
    #UnderlyingSecurityName          = None # NumberOfUnderlyingFund in PortfolioStatistics
    #PerformanceId                   = None # InvestmentVehicle/TrailingPerformance/MonthEndTrailingPerformance/PerformanceId
    LessThanOneYearBond              = None
    #ZAFBondIssuerClass               = None
    #IndianCreditQualityClassificatio = None
    #IndianIndustryClassification     = None
    #SurveyedWeighting                = None
    
    
    for event, element in iterable:
 
        tag = element.tag
        value = element.text
        
        if tag == "Portfolio" and event == "start" :
            _CurrencyId = element.attrib.get("_CurrencyId")
            Portfolio_ORDINAL += 1
        elif tag == "Portfolio" and event == "end" :
            Fund_Name           = None
            ShareClassId        = None
            Date                = None
            _CurrencyId         = None
        
        # Accessing a Portfolio Summary and saving data
        if tag == "PortfolioSummary" and event == "start" :
            PortfolioSummary_ORDINAL += 1
            
        elif tag == "PortfolioSummary" and event == "end" :
            tmp_list_PSX = [Filename,
                            Portfolio_ORDINAL,
                            Fund_Name,
                            ShareClassId,
                            Date,
                            _CurrencyId,
                            PortfolioSummary_ORDINAL,
                            NumberOfHoldingShort,      
                            NumberOfStockHoldingShort,
                            NumberOfBondHoldingShort, 
                            TotalMarketValueShort, 
                            NumberOfHoldingLong, 
                            NumberOfStockHoldingLong, 
                            NumberOfBondHoldingLong, 
                            TotalMarketValueLong]
        
            psx_cache.extend([';'.join(list(map(str, tmp_list_PSX)))])
            tmp_list_PSX = []
            
            if len(psx_cache) % 5000 == 0 :
                psx_handle.write('\n'.join([row for row in psx_cache]) + '\n')
                psx_handle.flush()
                psx_cache = []

            # Reset Values after Creating a Row
            NumberOfHoldingShort      = '0'
            NumberOfStockHoldingShort = '0'
            NumberOfBondHoldingShort  = '0'
            TotalMarketValueShort     = '0'
            NumberOfHoldingLong       = '0'
            NumberOfStockHoldingLong  = '0'
            NumberOfBondHoldingLong   = '0'
            TotalMarketValueLong      = '0'
        
        # Separating the different sections of the data
        if tag == "FundShareClass" and event == "start" :
            ShareClassId = element.attrib.get('_Id')
        
        if tag == "Name": Fund_Name = value

        if tag == "Date" : Date = value
        
        if tag == "HoldingAggregate" and event == "start" :
            if element.attrib.get("_SalePosition") == "L" :
                Section = "L"
            elif element.attrib.get("_SalePosition") == "S" :
                Section = "S"
        elif tag == "HoldingAggregate" and event == "end" :
            Section = None
        
        if tag == "Holding" and event == "start" :
            Holding_Ordinal = 0
        elif tag == "Holding" and event == "end" :
            del Holding_Ordinal
            
        if tag == "HoldingDetail" and event == "start" : 
            Section = "D"
            Holding_Ordinal += 1   
        elif tag == "HoldingDetail" and event == "end" :
            
            # Append row of data to list
            tmp_list_HDX = [Filename,
                            Portfolio_ORDINAL,
                            Fund_Name,
                            ShareClassId, 
                            Date,
                            _CurrencyId,
                            PortfolioSummary_ORDINAL,
                            Holding_Ordinal,
                            _DetailHoldingTypeId,
                            #_StorageId,
                            _ExternalId,
                            _Id,
                            #ExternalName,
                            Country_Id,
                            Country,
                            CUSIP,
                            SEDOL,
                            ISIN,
                            Ticker,
                            Currency,
                            Currency_Id,
                            SecurityName,
                            #LocalName,
                            Weighting,
                            NumberOfShare,
                            SharePercentage,
                            #NumberOfJointlyOwnedShare,
                            MarketValue,
                            CostBasis,
                            ShareChange,
                            Sector,
                            MaturityDate,
                            #AccruedInterest,
                            Coupon,
                            CreditQuality,
                            Duration,
                            IndustryId,
                            #GlobalIndustryId,
                            #GlobalSector,
                            #GICSIndustryId,
                            #LocalCurrencyCode,
                            #LocalMarketValue,
                            #ZAFAssetType,
                            PaymentType,
                            Rule144AEligible,
                            AltMinTaxEligible,
                            #BloombergTicker,
                            #ISOExchangeID,
                            #ContractSize,
                            #SecondarySectorId,
                            #CompanyId,
                            FirstBoughtDate,
                            #MexicanTipoValor,
                            #MexicanSerie,
                            #MexicanEmisora,
                            #UnderlyingSecId,
                            #UnderlyingSecurityName,
                            #PerformanceId,
                            LessThanOneYearBond]
            
            hdx_cache.extend([';'.join(list(map(str, tmp_list_HDX)))])
            tmp_list_HDX = []
            
            # Reset Values after Creating a Row
            _DetailHoldingTypeId             = None
            #_StorageId                      = None
            _ExternalId                      = None
            _Id                              = None
            #ExternalName                    = None
            Country_Id                       = None
            Country                          = None
            CUSIP                            = None
            SEDOL                            = None
            ISIN                             = None
            Ticker                           = None
            Currency                         = None
            Currency_Id                      = None
            SecurityName                     = None
            #LocalName                       = None
            Weighting                        = None
            NumberOfShare                    = '0'
            SharePercentage                  = None
            #NumberOfJointlyOwnedShare       = None
            MarketValue                      = '0'
            CostBasis                        = None
            ShareChange                      = '0'
            Sector                           = None
            MaturityDate                     = None
            #AccruedInterest                 = None
            Coupon                           = None
            CreditQuality                    = None
            Duration                         = None
            IndustryId                       = None
            #GlobalIndustryId                = None
            #GlobalSector                    = None
            #GICSIndustryId                  = None
            #LocalCurrencyCode               = None
            #LocalMarketValue                = None
            #ZAFAssetType                    = None
            PaymentType                      = None
            Rule144AEligible                 = None
            AltMinTaxEligible                = None
            #BloombergTicker                 = None
            #ISOExchangeID                   = None
            #ContractSize                    = None
            #SecondarySectorId               = None
            #CompanyId                       = None 
            FirstBoughtDate                  = None
            #MexicanTipoValor                = None
            #MexicanSerie                    = None
            #MexicanEmisora                  = None
            #UnderlyingSecId                 = None 
            #UnderlyingSecurityName          = None 
            #PerformanceId                   = None 
            LessThanOneYearBond              = None
            #ZAFBondIssuerClass               = None
            #IndianCreditQualityClassificatio = None
            #IndianIndustryClassification     = None
            #SurveyedWeighting                = None
            
            Section = None
            
            if len(hdx_cache) % 50000 == 0 :
                hdx_handle.write('\n'.join([row for row in hdx_cache]) + '\n')
                hdx_handle.flush()
                hdx_cache = []

        if Section == "L":
            if tag == "NumberOfHolding" : 
                if value == None :
                    NumberOfHoldingLong = '0'
                else :
                    NumberOfHoldingLong = value
            elif tag == "NumberOfStockHolding" :
                if value == None :
                    NumberOfStockHoldingLong = '0'
                else :
                    NumberOfStockHoldingLong = value
            elif tag == "NumberOFBondHolding" :
                if value == None :
                    NumberOfBondHoldingLong = '0'
                else :
                    NumberOfBondHoldingLong = value
            elif tag == "TotalMarketValue" :
                if value == None :
                    TotalMarketValueLong = '0'
                else :
                    TotalMarketValueLong = value
      
        elif Section == "S":
            if tag == "NumberOfHolding" : 
                if value == None :
                    NumberOfHoldingShort = '0'
                else :
                    NumberOfHoldingShort = value
            elif tag == "NumberOfStockHolding" :
                if value == None : 
                    NumberOfStockHoldingShort = '0'
                else :
                    NumberOfStockHoldingShort = value
            elif tag == "NumberOFBondHolding" :
                if value == None :
                    NumberOfBondHoldingShort = '0'
                else :
                    NumberOfBondHoldingShort = value
            elif tag == "TotalMarketValue" :
                if value == None :
                    TotalMarketValueShort = '0'
                else :
                    TotalMarketValueShort = value
                  
        elif Section == "D":
            if tag == "DetailHoldingTypeId" : _DetailHoldingTypeId = value
            elif tag == "HoldingDetail" :
                _ExternalId = element.attrib.get("_ExternalId")
                _Id = element.attrib.get("_Id")
            elif tag == "Country" :
                Country_Id = element.attrib.get("_Id")
                Country = value
            elif tag == "CUSIP"  : CUSIP  = value
            elif tag == "SEDOL"  : SEDOL  = value
            elif tag == "ISIN"   : ISIN   = value
            elif tag == "Ticker" : Ticker = value
            elif tag == "Currency" :
                Currency = value
                Currency_Id = element.attrib.get("_Id")
            elif tag == "SecurityName"        : SecurityName        = value
            elif tag == "Weighting"           : Weighting           = value
            elif tag == "NumberOfShare"       : 
                if value == None : NumberOfShare = '0'
                else : NumberOfShare = value
            elif tag == "SharePercentage"     : SharePercentage     = value
            elif tag == "MarketValue"         :
                if value == None : MarketValue = '0'
                else : MarketValue = value
            elif tag == "CostBasis"           : CostBasis           = value
            elif tag == "ShareChange"         :
                if value == None : ShareChange = '0'
                else : ShareChange = value
            elif tag == "Sector"              : Sector              = value
            elif tag == "MaturityDate"        : MaturityDate        = value
            elif tag == "Coupon"              : Coupon              = value
            elif tag == "CreditQuality"       : CreditQuality       = value
            elif tag == "Duration"            : Duration            = value
            elif tag == "IndustryId"          : IndustryId          = value
            elif tag == "PaymentType"         : PaymentType         = value
            elif tag == "Rule144AEligible"    : Rule144AEligible    = value
            elif tag == "AltMinTaxEligible"   : AltMinTaxEligible   = value
            elif tag == "FirstBoughtDate"     : FirstBoughtDate     = value
            elif tag == "LessThanOneYearBond" : LessThanOneYearBond = value
            
        # It's important to clear the elements when working with big datasets
        if event == "end": element.clear()
        
    if len(psx_cache) != 0 :
        psx_handle.write('\n'.join([row for row in psx_cache]) + '\n')
        psx_handle.flush()
        psx_cache = []

    if len(hdx_cache) != 0 :
        hdx_handle.write('\n'.join([row for row in hdx_cache]) + '\n')
        hdx_handle.flush()
        hdx_cache = []
        
    psx_handle.close()
    hdx_handle.close()