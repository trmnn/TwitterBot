import tweepy
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlescapy import sqlescape

def t_latest_feed(name):
  #twitter api token
  bearer_token = ""
  client = tweepy.Client(bearer_token)
  query = f'from:{name} -is:retweet -is:reply'
  response = client.search_recent_tweets(query=query,max_results=10,tweet_fields=['id','author_id', 'created_at','attachments'])
  #print(response.meta)
  tweets = response.data
  username=(client.get_users(ids=tweets[0].author_id)).data[0].name

  for n in range(2):
    date=str(tweets[n].created_at)
    dateFormat = str(f'{date[0:4]}-{date[5:7]}-{date[8:10]} {date[11:19]}')
    engine = create_engine('mysql://user:password@localhost/twitter',echo=True)
    with engine.connect() as con:
        tt = con.execute(sqlescape(f'SELECT ifnull((select TweetID from twitter where TweetID = "{tweets[n].id}"),"0");'))
        if not tt.first()[0]:
            print("Adding to database")
            rs=con.execute(f'INSERT INTO twitter (TweetID,Name,TweetDate,Content) VALUES ("{tweets[n].id}","{username[0:12]}","{dateFormat}","{sqlescape(tweets[n].text)}");')

if __name__ == "__main__":
  t = ["elonmusk",
       "VitalikButerin",
       "rogerkver",
       "aantop",
       "TimDraper",
       "SatoshiLite",
       "APompliano",
       "ErikVoorhees",
       "ToneVays",
       "officialmcafee",
       "IvanOnTech",
       "BVBTC",
       "danheld",
       "LayahHeilpern",
       "KennethBosak",
       "bhorowitz"]

  for item in t:
    try:
      t_latest_feed(item)
    except:
      print(f'User {item} did not post anything in a week')