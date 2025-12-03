from nsepython import equity_history

symbol = "SBIN"
series = "EQ"
start_date = "01-06-2024"
end_date ="08-06-2024"
print(equity_history(symbol,series,start_date,end_date))