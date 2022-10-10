# Notes about this study

## 1. GNO/USD
I was only able to get observations for GNO/USD for the timerange relative for this study (02/05/17 - 30/05/17) from Kraken. However, [Kraken's OHLC](https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData) endpoint will only get observations up to 720 days, or 3 years, before the time of the request.

I reached out to Kraken and their solution was to use their [downloadable historical market data](https://support.kraken.com/hc/en-us/articles/360047543791-Downloadable-historical-market-data-time-and-sales-) for the pair I would like to get data for.

The issue with this is that it is really just finding from their [Trades endpoint](https://docs.kraken.com/rest/#tag/Market-Data/operation/getRecentTrades). Meaning that it returns the price of the token for each trade.

This is more or less fine for the TWAP calculations since I am still getting 28 days of pricing data. If anything, it simply makes the TWAP value more sensitive than the others (higher variance). **However**, for the RSI and std_dev you should note that the `length` params were chosen with simple arithmatic `ceil(len(GNO_USD_prices) / 4)` just to make results of RSI and std_dev relative to the others.

Suggestions for an improvement are welcome, and the article will update the article once a better solution for this can be found.
