import tweepy
import redis
import pymongo

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

redis = redis.StrictRedis()
mongo = pymongo.MongoClient()
collection = mongo.twitter.tweets
user_collection = mongo.twitter.users

collection.create_index([('id', pymongo.ASCENDING)], unique = True)
user_collection.create_index([('id', pymongo.ASCENDING)], unique = True)

initialUsers = [
    27260086,
]

redis.sadd('users', *initialUsers)

while redis.scard('users') > 0:
    redis.delete('user_connections')
    uid = redis.spop('users')

    try:
        user = api.get_user(user_id = uid)
    except tweepy.TweepError as e:
        print(e)
        print('Error when looking up user {}'.format(uid))
        continue

    if user.protected:
        print('Skipping protected user {} (@{})'.format(user.name, user.screen_name))
        redis.sadd('users_done', uid)
        continue

    print('Downloading tweets for user {} (@{})'.format(user.name, user.screen_name))

    followers = api.followers_ids(user_id = uid)
    if followers:
        redis.sadd('user_connections', *followers)

    friends = api.friends_ids(user_id = uid)
    if friends:
        redis.sadd('user_connections', *friends)

    new_ids = redis.sdiff('user_connections', 'users_done')
    if new_ids:
        redis.sadd('users', *new_ids)

    alltweets = []
    try:
        tweets = api.user_timeline(user_id = uid, count = 200, trim_user = 1)
        alltweets.extend(tweets)

        oldest = tweets[-1].id - 1 if tweets else -1

        print("Downloaded {} tweets so far".format(len(alltweets)))
        while True:
            tweets = api.user_timeline(user_id = uid, count = 200, trim_user = 1, max_id = oldest)

            if not tweets:
                break

            alltweets.extend(tweets)

            oldest = tweets[-1].id - 1
            print("Downloaded {} tweets so far".format(len(alltweets)))
    except tweepy.TweepError:
        print("Couldn't download tweets for user")

    if alltweets:
        try:
            ujson = user._json
            ujson['followers'] = list(map(lambda f: {'id': f}, followers))
            ujson['friends'] = list(map(lambda f: {'id': f}, friends))
            user_collection.insert_one(ujson)
        except pymongo.errors.DuplicateKeyError:
            pass
        try:
            collection.insert_many(map(lambda t: t._json, alltweets), ordered = False)
        except pymongo.errors.DuplicateKeyError:
            pass

    redis.sadd('users_done', uid)
    redis.sadd('users_done_with_connections', uid)
