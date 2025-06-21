# alphavantage_server.py
import asyncio
import json
import os
import sys
from typing import Any, Sequence
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Get API key from environment
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("ALPHAVANTAGE_API_KEY environment variable is required")

server = Server("alphavantage")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_stock_quote",
            description="Get current stock quote",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_daily_prices",
            description="Get daily time series data for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_income_statement",
            description="Get annual income statement for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_balance_sheet",
            description="Get annual balance sheet for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_cash_flow",
            description="Get annual cash flow statement for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_company_overview",
            description="Get company overview and key metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_news_sentiment",
            description="Get latest news and sentiment for a stock or topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "tickers": {
                        "type": "string",
                        "description": "Stock symbol(s) separated by comma (e.g., AAPL,MSFT) or leave empty for general market news"
                    },
                    "topics": {
                        "type": "string",
                        "description": "Optional: News topics like 'earnings', 'merger', 'technology', etc."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of articles to return (default: 50, max: 1000)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_earnings",
            description="Get earnings data for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    async def make_api_request(url: str) -> dict:
        """Helper function to make API requests with error handling"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # Check for Alpha Vantage API errors
                if "Error Message" in data:
                    return {"error": f"API Error: {data['Error Message']}"}
                elif "Note" in data:
                    return {"error": f"API Limit: {data['Note']}"}
                elif "Information" in data:
                    return {"error": f"API Info: {data['Information']}"}

                return data
        except httpx.TimeoutException:
            return {"error": "Request timed out"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

    if name == "get_stock_quote":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_daily_prices":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_income_statement":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_balance_sheet":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_cash_flow":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_company_overview":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_news_sentiment":
        tickers = arguments.get("tickers", "")
        topics = arguments.get("topics", "")
        limit = arguments.get("limit", 50)

        # Build URL with optional parameters
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={API_KEY}&limit={limit}"

        if tickers:
            url += f"&tickers={tickers}"
        if topics:
            url += f"&topics={topics}"

        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    elif name == "get_earnings":
        symbol = arguments.get("symbol")
        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={API_KEY}"
        data = await make_api_request(url)
        return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alphavantage",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())