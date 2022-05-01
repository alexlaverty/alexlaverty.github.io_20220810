---
layout: post
title: Manly Beach Reddit Bot 
description: Creating a reddit bot for the Manly Beach subreddit written in Python
date: 2022-05-01
categories: [tech]
tags: [
  laverty
  ]
image:
  src: /assets/img/reddit-bot/thumbnail.png
  alt: Manly Beach Reddit Bot
hide_thumbnail: False
---

I was surfing Reddit and realised there wasn't a Manly Beach subreddit, so I decided to create one :

<https://www.reddit.com/r/manlybeach>

I was now the moderator of the Manly Beach subreddit, however the subreddit was looking quite bare and sad.

I thought it would take a long time for a community to build up around the subreddit if it just sat empty so I started searching for current news articles and posting them to the subreddit. I quickly realised that long term I didn't want spend my free time trawling the internet for relevant Manly Beach news articles to post to build up this subreddit so I started to think about writing a script to scrape websites and post for me. 

So I started where all good projects start by creating a repository on github.com :

<https://github.com/alexlaverty/manlybeach-reddit-bot>

I decided to write the script in Python and mainly used the following python libraries :

* [Pandas](https://pandas.pydata.org/) for data manipulation and analysis
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for parsing and extracting information from html 
* [Praw](https://praw.readthedocs.io/en/stable/) for sending requests to the Reddit API

First I went looking for websites that had articles relevant to Manly Beach and came up with the following list :

* <https://www.dailymail.co.uk>
* <https://www.9news.com.au/manly>
* <https://www.manlyaustralia.com.au/news/>
* <https://manlyobserver.com.au/category/latest-news/>
* <https://www.northernbeachesadvocate.com.au/?s=manly>
* <https://www.sproutdaily.com>
* <https://pacificjules.typepad.com/>

The way the script works is it uses the request library to connect to each url and download the websites html code, for example :

```Python3
remote_url = 'https://www.9news.com.au/manly'
page = urllib.request.urlopen(remote_url)
```

then we parse that html and create a BeautifulSoup object :

```Python3
soup = BeautifulSoup(page, 'html.parser')
```

The next thing we want to do is query this html and extract the articles titles and urls,

Browse the url :

https://www.9news.com.au/manly

Right click an articles title and click `inspect` which the inspecter shows up you can determine the articles html element, 

<img src="/assets/img/reddit-bot/inspect.png">


in this case the articles element is a H3 with a class called `story__headline`, we can then query for this element using the following :

```Python3
headlines = soup.find_all('h3', {'class' : 'story__headline'})
```

next we can loop through each of these articles and extract out the article title and the url, and then we'll store these titles and urls in a Pandas Dataframe :

``` Python3
df = pd.DataFrame(columns=["timestamp","title", "url","posted"])

for headline in headlines:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title=headline.find('span', {'class' : 'story__headline__text'}).text
        try:

            url = headline.find('a')['href']
            #print(title, url)
            df = df.append({
                 "timestamp": timestamp,
                 "title": title,
                 "url": url,
                 "posted": "False",
            }, ignore_index=True)
        except TypeError:
            pass
```

If you print out the dataframe and it will look a lot like an excel spreadsheet with columns and rows :

```
2022-05-01 16:03:17,Sydney neighbour's $120k defamation payout over 'busybody' comment overturned,https://www.9news.com.au/national/manly-apartment-defamation-payout-gary-raynor-sued-patricia-murray-overturned-sydney-news/24ca00b8-85c2-43a3-a80d-15df6048b630,False
2022-05-01 16:03:17,Wife of ex-NRL player fined over unrestrained toddler cover-up,https://www.9news.com.au/national/john-hopoate-wife-in-court-over-unrestrained-toddler-car-video-nrl-news/4a3ccaa4-0dcd-4b9b-ae62-dc9457581a04,False
2022-05-01 16:03:17,Authorities confirm Manly swimmer was attacked by a shark,https://www.9news.com.au/national/man-attacked-by-shark-at-manly-beach-sydney-news/a795fc0f-0863-49ef-ac78-85c4ae5a9c46,False
2022-05-01 16:03:17,'He’s scaring me': Distressing video of NRL star's arrest,https://www.9news.com.au/national/dylan-walker-disturbing-video-shows-night-manly-player-arrested-for-domestic-violence/367b4725-5a4e-40c2-a5d3-2c0ff4c315df,False
2022-05-01 16:03:17,Two arrested after North Sydney suburbs placed in lockdown ,https://www.9news.com.au/national/manly-vale-sydney-suburb-lock-down-police-operation/d4ab02aa-7748-4068-b94e-98959b3ed83b,False
```

The columns are the date the article was scraped, the article title, the url, and the final column is whether the url has been posted to reddit or not, when first scraped this value is set to False, once posted to reddit this value is updated to True.

From here we append the dataframe to a CSV file called `data.csv`, once appended we drop duplicate urls, this way if a link has already been posted to reddit it won't be added again :

```
csv = csv.append(df, ignore_index=True)
csv.drop_duplicates(['url'],inplace=True)
csv.to_csv(csv_file, index=False)
```

Once all the websites have been scraped and articles added the spreadsheet the next step is to post the articles to Reddit which we do via the publish_to_reddit() function :

```
def publish_to_reddit():
    username      = os.getenv('REDDIT_USERNAME')
    password      = os.getenv('REDDIT_PASSWORD')
    sub_reddit    = os.getenv('REDDIT_SUB_REDDIT')
    client_id     = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent    = os.getenv('REDDIT_USER_AGENT')
    csv = pd.read_csv(csv_file)
    print("Publishing to Subreddit : {}".format(sub_reddit))
    print("==================================")
    reddit = praw.Reddit(username=username,
                         password=password,
                         client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent
                         )

    for index, row in csv.iterrows():
        if row['posted'] == False:
            title=row['title']
            url=row['url']
            print("Title : {}".format(title))
            print("URL : {}".format(url))
            wait_for=randint(600, 900)
            try:
                reddit.subreddit(sub_reddit).submit(title[:300], url=url)
                print("POSTED TO REDDIT!")
                csv.at[index,'posted'] = "True"
                csv.to_csv(csv_file, index=False)
                print("Waiting for random ammount of seconds before posting again : {}".format(str(wait_for)))
                sleep(wait_for)
            except TypeError as error:
                print(error)
                pass
            print("----------------------------------")
```

The way this function works is it reads the `data.csv` file, loop through each row, if the row hasn't been posted to reddit `if row['posted'] == False:` then 

it attemps to use the praw library to post to reddit and then updates its post status to True :

```
reddit.subreddit(sub_reddit).submit(title[:300], url=url)
csv.at[index,'posted'] = "True"
```

`title[:300]` will truncate the reddit post title to 300 characters because that's the limit for the title length, anything over that will throw an error.

Reddit will throttle you and return errors if you try and post too quickly so I have added in some code to wait for a random ammount of time between 10 and 15 minutes before attempting to post again :

```
wait_for=randint(600, 900)
sleep(wait_for)
```

The user, password, tokens, secrets etc are set as environment variables so that they are not stored in code to prevent leaking credentials :

```
username      = os.getenv('REDDIT_USERNAME')
password      = os.getenv('REDDIT_PASSWORD')
sub_reddit    = os.getenv('REDDIT_SUB_REDDIT')
client_id     = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent    = os.getenv('REDDIT_USER_AGENT')
```

This script is now able to run locally to scrape and post articles but I want to automate this script to run on a schedule and I don't want to have my computer turned on all the time.

Github has something called [Github Actions Workflows](https://docs.github.com/en/actions/using-workflows) which allows you to setup a scheduled job.

To do this created a file in the folder path :

```
.github/workflows/reddit.yaml
```

The content of the file is as follows :

```
# Give your gitflow action a name
name: Manly Beach Reddit

# Set a schedule to run, note it's in UTC time, so do the time conversion for your location
on:
  schedule:
    - cron: '0 */12 * * *' # runs every 12 hours

# Also run the build if I push anything into the master branch
  push:
    branches:
      - master
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: checkout repo content
        uses: actions/checkout@v2 # checkout the repository content to github runner.

      - name: setup python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9 #install the python needed
         
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
      - name: execute py script # run the run.py to get the latest data
        run: |
          python app.py
        env:
          REDDIT_USERNAME: ${{ secrets.REDDIT_USERNAME }}
          REDDIT_PASSWORD: ${{ secrets.REDDIT_PASSWORD }}
          REDDIT_SUB_REDDIT: ${{ secrets.REDDIT_SUB_REDDIT }}
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          REDDIT_USER_AGENT: ${{ secrets.REDDIT_USER_AGENT }}

      - name: Git Push Updates
        run: |
          [[ -z $(git status -s) ]] || (
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "ManlyBeach Scheduled Update" -a
          git push -f)
```

The job is scheduled to run twice a day :

```
# Set a schedule to run, note it's in UTC time, so do the time conversion for your location
on:
  schedule:
    - cron: '0 */12 * * *' # runs every 12 hours
```

The reddit.yaml file is pretty self explanatory, the job checks out the repository, installs the Python dependecies, runs the script and passes in the Reddit api secrets which were defined as Github secrets, after the script runs if there are any updates to the files, for example new url's have been added to the `data.csv` git will commit those changes to the github repository, this is to persist the status of whether the url's have been posted to reddit for the next time the job runs, this will prevent duplicate articles being posted.

If you go to the repositories Actions tab you can see the build logs and status history of previous builds :

<img src="/assets/img/reddit-bot/actions.png" alt="Github Actions">

Once the build successfully completes you can browse the Manly Beach subreddit and see if your posts have been submitted :

<https://www.reddit.com/r/ManlyBeach/>

<img src="/assets/img/reddit-bot/manly-beach-subreddit.png" alt="Manly Beach Subreddit">

If you want to see a website added to the list to be posted to the subreddit leave a comment below.

If you want to have a go at coding it yourself feel free to raise a pull request here :

<https://github.com/alexlaverty/manlybeach-reddit-bot/pulls>