import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))
from datetime import date
current_date = date.today()
# SAMPLE_ASSET_DATA = [
#     {
#         "name": "Gold",
#         "type": "asset_class",
#         "description": "Precious metal commodity",
#         "sub_classes": ["Physical Gold", "Gold ETFs", "Gold Mining Stocks"],
#     },
#     {
#         "name": "Apple Inc",
#         "type": "security_name",
#         "sector": "Technology",
#         "sub_sector": "Consumer Electronics",
#     },
#     {
#         "name": "US Equities",
#         "type": "asset_class",
#         "description": "United States listed stocks",
#         "sub_classes": ["Large Cap", "Mid Cap", "Small Cap"],
#     }
# ]

SAMPLE_ASSET_DATA = [
    {
        "name": "Cash and Cash Equivalents",
        "type": "asset_class",
        "description": "This asset class contains the following sub-asset classes: Accrual Accounts, Cash Equivalents, Current Accounts, Deposits, Margin accounts, Money Market Funds"
    },
    {
        "name": "Accrual Accounts",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Cash Equivalents",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Current Accounts",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Deposits",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Margin accounts",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Money Market Funds",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Cash and Cash Equivalents"
    },
    {
        "name": "Commodity",
        "type": "asset_class",
        "description": "This asset class contains the following sub-asset classes: Commodities- Bullion Balances, Commodities- Physical, Commodity - Forwards/Swaps/Options/Accumulative Forwards, Commodity Derivatives, Commodity ETFs, Commodity Funds, Commodity Structured Products, Gold, Livestock, Oil, Rubber, Silver, Unclassified"
    },
    {
        "name": "Commodities- Bullion Balances",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodities- Physical",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodity - Forwards/Swaps/Options/Accumulative Forwards",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodity Derivatives",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodity ETFs",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodity Funds",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Commodity Structured Products",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Gold",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Livestock",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Oil",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Rubber",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Silver",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Unclassified",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Commodity"
    },
    {
        "name": "Contingent Liabilities",
        "type": "asset_class",
        "description": "This asset class contains the following sub-asset classes: Contingent Liabilities"
    },
    {
        "name": "Contingent Liabilities",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Contingent Liabilities"
    },
    {
        "name": "Digital Asset",
        "type": "asset_class",
        "description": "This asset class contains the following sub-asset classes: Cryptocurrency, NFT"
    },
    {
        "name": "Cryptocurrency",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Digital Asset"
    },
    {
        "name": "NFT",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Digital Asset"
    },
    {
        "name": "Equities",
        "type": "asset_class",
        "description": "This asset class contains the following sub-asset classes: Equity Accu/Deccu, Equity Derivatives, Equity ETF, Equity Funds, Equity Structured Products, Equity Unlisted, Index Option, Listed Equities, Preference Shares, Private Equity"
    },
    {
        "name": "Equity Accu/Deccu",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Equity Derivatives",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Equity ETF",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Equity Funds",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Equity Structured Products",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Equity Unlisted",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Index Option",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Listed Equities",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Preference Shares",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    },
    {
        "name": "Private Equity",
        "type": "asset_sub_class",
        "description": "This asset sub-class belongs to Equities"
    }
]
asset_with_subtypes = [
  "Cash and Cash Equivalents: Accrual Accounts, Cash Equivalents, Current Accounts, Deposits, Margin accounts, Money Market Funds",
  "Commodity: Commodities- Bullion Balances, Commodities- Physical, Commodity - Forwards/Swaps/Options/Accumulative Forwards, Commodity Derivatives, Commodity ETFs, Commodity Funds, Commodity Structured Products, Gold, Livestock, Oil, Rubber, Silver, Unclassified",
  "Contingent Liabilities: Contingent Liabilities",
  "Digital Asset: Cryptocurrency, NFT",
  "Equities: Equity Accu/Deccu, Equity Derivatives, Equity ETF, Equity Funds, Equity Structured Products, Equity Unlisted, Index Option, Listed Equities, Preference Shares, Private Equity",
  "Fixed Income: Asset Backed Securities, Bonds, Callable Bonds, Convertible bonds, Fixed Bonds, Fixed Income Derivatives, Fixed Income ETFs, Fixed Income Funds, Fixed Income Structured Products, Fixed Income Unlisted, Floating Bonds, Interest Rate Derivatives, Notes, Preference Shares",
  "Forex: Dual Currency Investments, FX Derivatives, FX Derivatives - Forwards, FX Derivatives - Forwards/Swaps/Options/Acc Forwards, FX Derivatives - TRF, FX ETFs, FX Structured Products",
  "Hybrid: Balanced Fund",
  "Insurance: Insurance",
  "IRS: IRS",
  "Liabilities: Credit Facilities, Guarantees, Loans, Non-Investment Loans, Overdrafts, Unclassified Liabilities",
  "Multi-Asset & Alternative Investments: Balanced Funds, Convertible Funds, Dual Currency Investments, Hedge Funds, Liquid Alternatives, Mutual fund, Other Derivatives, Other ETFs, Other Funds, Private Equity, Private Equity Fund, Rates/Swaps, Real Estate, REITs, Structured Products Unclassified, Structured Products with Other Underlyings, Unclassified Assets",
  "Non-Investment Assets: Non-Investment Assets",
  "Others: Others, Unclassified Assets",
  "Rates: Interest Rate ETFs, Interest Rate Funds, Rates Structured Products",
  "Real Estate Fund: Real Estate"
]

news_query = f"""Fetch the latest financial news in last 24 hours from current date {current_date} about Cash and cash equivalents , commodity , contingeont liabilities , digital assets , equities , fixed income , forex , Hybrid asset , insurance , IRS , Liabilities , Multi-Asset & Alternative Investments , Non-investment Assets, Rates , Real estate fund"""

analyze_news_prompt = f"""You are an expert financial analysis agent specializing in real-time market analysis. Your task is to analyze the provided financial news data and provide comprehensive insights for various financial instruments and asset classes.

AVAILABLE ASSETS AND CLASSIFICATIONS:
{asset_with_subtypes}

OBJECTIVE:
Analyze the provided news for all relevant assets, asset classes, and instruments mentioned. For each one, provide:
- Current market conditions and price movements
- Market sentiment analysis
- Key events or announcements
- Trading volumes where relevant
- Current trends and patterns
- Expert opinions and consensus
- Notable predictions or forecasts

INSTRUCTIONS:
1. Carefully analyze all provided news data
2. Identify all mentioned assets, asset classes, and financial instrument based on the available assets and classifications given
3. Provide clear positive/negative/neutral signals based on evidence
4. Support confidence ratings with concrete data points
5. Include current prices and percentage changes where available
6. List key events affecting each asset/instrument

CRITICAL :
Focus only on news from the last 24 hours current date is {current_date}
Consider the available assets and classification in the value for the key name in the object in the output format

OUTPUT FORMAT:
Return an array of objects, where each object follows this exact structure:
[
    {{
        "name": "exact name of asset/class/instrument that should be taken from the available assets and classifications if not available then don't create this object at all",
        "type": "asset_class|asset_sub_class|instrument_name",
        "analysis": "positive|negative|neutral",
        "confidence": "number between 0 and 1",
        "reasoning": "Brief explanation backed by specific news/data",
        "price": "current price if available",
        "percentage_change": "24h change in percentage",
        "key_events": ["event1", "event2", "event3"],
        "date_analyzed": "current date in YYYY-MM-DD format"
    }},
    ...
]

IMPORTANT GUIDELINES:
- Only include assets/instruments mentioned in the news data
- Ensure "type" field is exactly one of: asset_class, asset_sub_class, or instrument_name
- Provide confidence ratings based on news volume and consistency
- Include specific numbers and percentages whenever available
- List multiple key events when possible
- Keep reasoning concise but informative
- Format dates consistently as YYYY-MM-DD

Analyze the provided news data and generate the response in the exact format specified above."""

