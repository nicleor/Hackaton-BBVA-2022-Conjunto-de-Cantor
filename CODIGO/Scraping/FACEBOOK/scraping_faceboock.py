from facebook_scraper import get_posts
from twitter_scraper import get_tweets

all_post = get_posts("kubofinanciero", pages = 5)
#print(all_post)

#for post in all_post:
#    print(post)

for post in get_posts('nintendo',pages=3):
    print(post['text'])

#for tweet in get_tweets('@MxNintendo',pages=3):
#    print (tweet['text'])