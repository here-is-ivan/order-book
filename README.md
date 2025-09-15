objective:
build a python script that will get data from different crypto exchanges and find the best price to buy and sell a certain amount of bitcoin

steps:
1. get data of order books from coinbase api (https://api.exchange.coinbase.com/products/BTC-USD/book?level=2) and from gemini api (https://api.gemini.com/v1/book/BTCUSD)
2. normalize the requested data into the following format:
    bids = [[price, size], ...]  # sorted descending
    asks = [[price, size], ...]  # sorted ascending
3. calculate the lowest price to buy X amount of bitcoin (10 BTC by default) and calculate the highest price to sell X amount of bitcoin (10 BTC by default) 
4. return the result in following format:
    To buy 10 BTC: $XXX,XXX.XX
    To sell 10 BTC: $YYY,YYY.YY
5. add a command line parameter "--qty" so the script can be run with a custom amount of bitcoin 
6. implement a custom rate limiter (max 1 call per exchange per 2 seconds, no time.sleep)

constraints:
- use requests, httpx, or aiohttp
- no AI to complete the task

thoughts:
- if one of the apis doesn't return 200 status code, should the execution stop without returning anything or should it continue with data only from one api?
- i assume that there will always be the enough amount of bitcoin on these order books but what should the script return in case there's not enough orders to get to the desired amount of crypto?
- i assume that the execution speed is important here because if you actually want to sell or buy at the best price, you have to be first. it means that bids and asks from each api should be compared one by one in a loop when appended instead of appending everything to one array and then sorting, so we can reach O(n) time complexity instead of (n log n). the task says that i have to normalize the data into separate lists first and then return the result. its good for readability to do it that way and wrap it in a function but you don't need the whole data response to be converted into new arrays if the speed is crucial. you create new arrays which requires more memory and you most definitely to keep appending bids and asks even when its enough data to return the output. i will stick to the separate lists and data normalization because its explicitly said in the task description 