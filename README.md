# Alpha Vantage MCP Server

A Model Context Protocol (MCP) server that provides access to Alpha Vantage financial data APIs for use with Claude Desktop and other MCP-compatible applications.

## 🚀 Features

- **Stock Data**: Real-time quotes and historical daily prices
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Company Information**: Company overviews and earnings data
- **News & Sentiment**: Latest financial news with sentiment analysis
- **Error Handling**: Robust API error handling and rate limit management

### Configuration

1. Get your free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```
3. Add your API key to the `.env` file:
   ```
   ALPHAVANTAGE_API_KEY=your_api_key_here
   ```

> [!NOTE]
> **Priority**: Environment variables set in `claude_desktop_config.json` take precedence over `.env` files. To use `.env`, remove the key from your Claude Desktop config.

### Usage with Claude Desktop

## 📋 Prerequisites

1. **Alpha Vantage API Key**: Get your free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. **Python 3.8+**: Make sure you have Python installed
3. **Claude Desktop**: Or another MCP-compatible application

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/alphavantage-mcp-server.git
cd alphavantage-mcp-server
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your API Key
1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free account
3. Copy your API key

## ⚙️ Configuration

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "alphavantage": {
      "command": "python3",
      "args": ["/path/to/alphavantage_server.py"],
      "env": {
        "ALPHAVANTAGE_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

**Important**: Replace `/path/to/alphavantage_server.py` with the actual path to your script and `your_actual_api_key_here` with your Alpha Vantage API key.

## 🎯 Usage Examples

Once configured, you can ask Claude:

- "Get the current stock quote for Apple (AAPL)"
- "Show me Microsoft's latest income statement"
- "What's the latest news about Tesla stock?"
- "Get Amazon's balance sheet data"
- "Show me Google's cash flow statement"

## 📊 Available Functions

| Function | Description |
|----------|-------------|
| `get_stock_quote` | Current stock price and basic metrics |
| `get_daily_prices` | Historical daily price data |
| `get_income_statement` | Annual income statements |
| `get_balance_sheet` | Annual balance sheet data |
| `get_cash_flow` | Annual cash flow statements |
| `get_company_overview` | Company fundamentals and key metrics |
| `get_news_sentiment` | Latest news with sentiment analysis |
| `get_earnings` | Quarterly and annual earnings data |

## 🔧 Testing

Test your installation by running the server directly:

```bash
export ALPHAVANTAGE_API_KEY="your_api_key"
python3 alphavantage_server.py
```

The server should start without errors. Press `Ctrl+C` to stop.

## 📝 API Limits

- **Free Tier**: 25 requests/day for premium endpoints, 500 requests/day for standard endpoints
- **Rate Limit**: 5 calls/minute
- **Premium Tiers**: Available for higher limits

## 🐛 Troubleshooting

### Common Issues

1. **"Server disconnected" error**
   - Check that your API key is correct
   - Verify the file path in your config
   - Ensure dependencies are installed

2. **"ModuleNotFoundError: No module named 'mcp'"**
   - Install dependencies: `pip install -r requirements.txt`
   - Use the correct Python path in your config

3. **API rate limit errors**
   - You've exceeded the free tier limits
   - Wait for the rate limit to reset or upgrade your plan

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing the financial data API
- [Anthropic](https://www.anthropic.com/) for creating the Model Context Protocol
- The MCP community for tools and documentation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [GitHub issues](https://github.com/yourusername/alphavantage-mcp-server/issues)
3. Create a new issue with detailed information about your problem

---
