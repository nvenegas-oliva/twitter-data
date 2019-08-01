
import sys
import configparser
import tweepy
import json


def get_all_tweets(screen_name):
    """
    Twitter only allows access to a users most recent 3240 tweets with this method
    """
    # Twitter API credentials
    config = configparser.ConfigParser()
    config.read('setup.ini')

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(config['twitter_api']['consumer_key'],
                               config['twitter_api']['consumer_secret'])
    auth.set_access_token(config['twitter_api']['access_key'],
                          config['twitter_api']['access_secret'])
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    alltweets = [tweet._json for tweet in alltweets]

    with open('tweets_%s.json' % screen_name, 'w') as fout:
        json.dump(alltweets, fout)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets(sys.argv[1])
