import tweepy
from service_metadata import twitter_credentials as twitter


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(twitter['api_key'], twitter['api_secret'])
    auth.set_access_token(twitter['access_token_key'], twitter['access_token_secret'])
    api = tweepy.API(auth)
    all_tweets = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items():
            all_tweets.append(tweet.text.encode('utf-8'))
        # changed cause it will produce empty list on error
        #  all_tweets = [item.text.encode('utf-8') for item in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items()]
    except tweepy.TweepError:
        print 'Twitter parsing error'
    return all_tweets


if __name__ == '__main__':
    print get_all_tweets('pontifex')
