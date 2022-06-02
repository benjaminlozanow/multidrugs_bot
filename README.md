# Drug-drug Interaction Twitter Bot

In this project I developed a Twitter bot that periodically tweets about possible interactions between common drugs. It also has the functionality to check if there is an interaction when the bot is mentioned (tagged) and two drugs are provided.

*Drug interactions occur when a drug's mechanism of action is disturbed by the concomitant administration substances such as foods, beverages or other drugs.*  
\- [Wikipedia](https://en.wikipedia.org/wiki/Drug_interaction#:~:text=Drug%20interactions%20occur%20when%20a,foods%2C%20beverages%20or%20other%20drugs.)  

## Bot's characteristics 

The bot is linked to the following account: https://twitter.com/multidrugsbot and was possible using the Twitter's [Developer Platform](https://developer.twitter.com/).

![pic](/img/twitter_account.png)

The bot was developed in python using primarly the [Tweepy](https://www.tweepy.org/) package to access the Twitter API.  

The bot consumes the [NIH API](https://lhncbc.nlm.nih.gov/RxNav/APIs/InteractionAPIs.html#:~:text=The%20Interaction%20API%20is%20a,contained%20in%20a%20JAMIA%20article.) using the DrugBank database in order to retrieve drugs' ID and check possible interactions between them.  

It is currently hosted in a [Heroku](https://www.heroku.com/) server, configured to continually run using the [Procfile](https://github.com/benjaminlozanow/multidrugs_bot/blob/main/Procfile).

## Functionalities

Periodic tweet: Tweet the interaction between two common drugs.
![pic2](/img/twitter_tweet.png)

Interaction checker: Reply if there is an interaction between two given drugs. And like their tweet.
![pic3](/img/twitter_reply.png)  

## Files

- The [multidrugs_bot.py](https://github.com/benjaminlozanow/multidrugs_bot/blob/main/multidrugs_bot.py) is the main script that gives the bot its functionalities.

- [last_seen_id.txt](https://github.com/benjaminlozanow/multidrugs_bot/blob/main/last_seen_id.txt) is a text-based "database" which keeps track of the latest tweet's ID corresponding to the last tweet processed by the bot (so it no longer reply those tweets).  

- [Procfile](https://github.com/benjaminlozanow/multidrugs_bot/blob/main/Procfile) is a file needed to run the main script in the Heroku server.