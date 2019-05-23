# Who are we really talking about? Trump Vs Clinton, a Twitter Sentiment Analysis

The race to the 2016 presidential election is going strong, there is a lot of talk and the general public opinion is up for grabs.The data for this endeavor is being pulled from the Twitter Streaming API.

I did not embed my ipython notebook here but you can see this project in full flow with live visualisations and a walk through at my blog, [Far Beyond Data] (https://guneetkohli.github.io/twitter-sentiment-analysis.html). Visualisations are based on interactive d3.js charts (plot.ly) which are updated every 6 hours as the scripts runs on my DigitalOcean cloud machine.

scraper.py scrapes twitter data and scans for terms in settings.py. Tweets get scraped into a DB file. DB is then converted to CSV. I have modified the scraper to run for 30 seconds and then quit. You can remove that and run it manually as needed, using Ctrl+c to stop scraping.

<h2> Installation </h2>
<li> pip3 install -r requirements.txt </li>
     psycopg2 installation would require postgresql client installation. 

<h2> Setup </h2>
<ul>
<li> Sign up for Twitter Developer account. Create a file called private.py and set the following keys </li>
    <ul>
    <li> TWITTER_KEY </li>
    <li> TWITTER_SECRET </li>
    <li> TWITTER_APP_KEY </li>
    <li> TWITTER_APP_SECRET </li>
    </ul>
<li> Set CONNECTION_STRING in settings.py. You can use sqlite:///tweets.db as default. </li>
<li> Edit settings.py to change behavior. </li>
</ul>

<h2> Use </h2>
<ul>
<li> python3 scraper.py --- scrapes data. </li>
<li> python3 dump.py --- generates CSV file which contains all data that was scraped. </li>
<li> python3 analysis.py --- analysis data by tweet numbers, content, location and sentiment </li>
</ul> 
<br>






    
    






