import requests_oauthlib
import requests 
import webbrowser
import json
import test106 as test 

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


client_key = 'NlfjkaAngNToFNPFTpUXLW3TY' 
client_secret = 'ybjzEDYKoOwyBdo0yswdLCofyeiuXZC8B1geuYCbTBwphWXfxS' 

if not client_secret or not client_key:
    print "You need to fill in client_key and client_secret. See comments in the code around line 8-14"
    exit()

def get_tokens():
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url)

    verifier = raw_input('Please input the verifier>>> ')

    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)
                              
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

try:
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens

protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)



r = oauth.get("https://api.twitter.com/1.1/search/tweets.json", 
                params = {'q': 'Trump', 'count' : 100})

res = r.json()


pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))


class Post():
    """object representing a tweet"""                          
    def __init__(self, post_dict={}):
        chars_to_remove = [u".",u",",u"!",u"?",u"'",u"@",u"#",u"$",u"%",u"&",u"*",u":",u";",u"-"]
        if 'text' in post_dict:
            text = post_dict['text'].lower() 
        else:
            text = ""
        for punc in chars_to_remove:
            text = text.replace(punc,u"")
            self.text = text 

    def positive(self):
        pos_words = []
        for word in self.text.split():
            if word in pos_ws:
                pos_words.append(word)
        return len(pos_words) 

    def negative(self):
        neg_words = []
        for word in self.text.split():
            if word in neg_ws:
                neg_words.append(word)
        return len(neg_words)

    def emo_score(self):
        pos_words = []
        for word in self.text.split():
            if word in pos_ws:
                pos_words.append(word)
        neg_words = []
        for word in self.text.split():
            if word in neg_ws:
                neg_words.append(word)

        score = len(pos_words) - len(neg_words)
        return score 


a = {"text": "abnormal! abolish abominable abominably abominate youthful zeal zest zippy"}
b = Post(a)

try:
    print "testing whether the Post class methods negative, postive, and emo_score do the right thing"
    test.testEqual(b.negative(), 5)
    test.testEqual(b.positive(), 4)
    test.testEqual(b.emo_score(), -1)

except:
    print "failed test for one or more Post class methods"
        


tweet_insts = []
for each_tweet in res['statuses']:
    tweet_insts.append(Post(each_tweet))


try:
    print "testing whether the list tweet_insts exists and is the right kind of thing"
    test.testEqual(type(tweet_insts), type([]))
    test.testEqual(len(tweet_insts) > 0, True)
    test.testEqual(type(tweet_insts[0]),type(Post()))
except:
    print "there is something wrong with tweet_insts"


emo_score_list = []
for tweet in tweet_insts:
    emo_score_list.append(tweet.emo_score())


def keep_positive(nums):
    pos_emo_scores = [num for num in nums if num > 0]
    return pos_emo_scores

def keep_negative(nums):
    neg_emo_scores = [num for num in nums if num < 0]
    return neg_emo_scores

def keep_neutral(nums):
    neutral_emo_scores = [num for num in nums if num == 0]
    return neutral_emo_scores

positive_tweets = len(keep_positive(emo_score_list))
negative_tweets = len(keep_negative(emo_score_list))
neutral_tweets = len(keep_neutral(emo_score_list))



if positive_tweets > negative_tweets:
    print "There are more positive tweets than negative tweets about Trump"
elif positive_tweets < negative_tweets:
    print "There are more negative tweets than positive tweets about Trump"
elif neutral_tweets > positive_tweets and negative_tweets:
    print "There are more neutral tweets about Trump"

emo_scores_dict = {}
for num in emo_score_list:
    if num in emo_scores_dict:
        emo_scores_dict[num] += 1
    else:
        emo_scores_dict[num] = 1

sorted_emo_scores_dict = sorted(emo_scores_dict.keys(), key = lambda x: emo_scores_dict[x], reverse = True)
top_emo_score = sorted_emo_scores_dict[0]
print "The most frequent emo score was" , top_emo_score

mean_emo = sum(emo_score_list)/100
print "The mean emo score was" , mean_emo


outfile = open('TwitterEmoScores.csv', 'w')
outfile.write('Emo Score\n')
for tweet in tweet_insts:
    outfile.write('%d\n' % (tweet.emo_score()))
outfile.write('Pos Tweets, Neg Tweets, Neutral Tweets, Top Emo Score, Mean Emo Score\n')
outfile.write('%d, %d, %d, %d, %d\n' % (positive_tweets, negative_tweets, neutral_tweets, top_emo_score, mean_emo))
outfile.close() 


# NEW YORK TIMES-----------------------------------------------------------------------------

nyt = requests.get('http://api.nytimes.com/svc/search/v2/articlesearch.json?q=trump&fq=headline%3A%28%22Trump%22%29&begin_date=20140101&sort=newest&fl=headline&api-key=df6a4f77f64423a136aaa0bd726844da%3A0%3A73697352')
articles = nyt.json()


class Score():

    def __init__(self, article_dict={}):
        chars_to_remove = [u".",u",",u"!",u"?",u"'",u"@",u"#",u"$",u"%",u"&",u"*",u":",u";",u"-"]
        if 'headline' in article_dict:
            headline = article_dict['headline']['main'].lower() 
            for punc in chars_to_remove:
                headline = headline.replace(punc,u"")
                self.headline = headline 


    def positive(self):
        pos_words = []
        for word in self.headline.split(): 
            if word in pos_ws:
                pos_words.append(word)
        return len(pos_words) 

    def negative(self):
        neg_words = []
        for word in self.headline.split():
            if word in neg_ws:
                neg_words.append(word)
        return len(neg_words)

    def emo_score(self):
        pos_words = []
        for word in self.headline.split():
            if word in pos_ws:
                pos_words.append(word)
        neg_words = []
        for word in self.headline.split():
            if word in neg_ws:
                neg_words.append(word)

        score = len(pos_words) - len(neg_words)
        return score 


a = {"headline": {"main":"abnormal! abolish abominable abominably abominate youthful zeal zest zippy"}}
b = Score(a)

try:
    print "testing whether the Score class methods negative, postive, and emo_score do the right thing"
    test.testEqual(b.negative(), 5)
    test.testEqual(b.positive(), 4)
    test.testEqual(b.emo_score(), -1)

except:
    print "failed test for one or more Score class methods"


headline_insts = []
for each_article in articles['response']['docs']:
    headline_insts.append(Score(each_article))

try:
    print "testing whether the list headline_insts exists and is the right kind of thing"
    test.testEqual(type(headline_insts), type([]))
    test.testEqual(len(headline_insts) > 0, True)
    test.testEqual(type(headline_insts[0]),type(Score()))
except:
    print "There is something wrong with headline_insts"


NYTemo_score_list = []
for each_headline in headline_insts:
    NYTemo_score_list.append(each_headline.emo_score())


positive_headlines = len(keep_positive(NYTemo_score_list))
negative_headlines = len(keep_negative(NYTemo_score_list))
neutral_headlines = len(keep_neutral(NYTemo_score_list))


if positive_headlines > negative_headlines:
    print "There are more positive headlines than negative headlines about Trump"
elif positive_headlines < negative_headlines:
    print "There are more negative headlines than positive headlines about Trump"
elif neutral_headlines > positive_headlines and negative_headlines:
    print "There are more neutral headlines about Trump"

NYTemo_scores_dict = {}
for num in NYTemo_score_list:
    if num in NYTemo_scores_dict:
        NYTemo_scores_dict[num] += 1
    else:
        NYTemo_scores_dict[num] = 1

NYTsorted_emo_scores_dict = sorted(NYTemo_scores_dict.keys(), key = lambda x: NYTemo_scores_dict[x], reverse = True)
NYTtop_emo_score = NYTsorted_emo_scores_dict[0]
print "The most frequent emo score was" , NYTtop_emo_score

NYTmean_emo = sum(NYTemo_score_list)/100
print "The mean emo score was" , NYTmean_emo



outfile = open('NYTEmoScores.csv', 'w')
outfile.write('Emo Score\n')
for each_headline in headline_insts:
    outfile.write('%d\n' % (each_headline.emo_score()))
outfile.write('Pos Headlines, Neg Headlines, Neutral Headlines, Top Emo Score, Mean Emo Score\n')
outfile.write('%d, %d, %d, %d, %d\n' % (positive_headlines, negative_headlines, neutral_headlines, NYTtop_emo_score, NYTmean_emo))
outfile.close() 





  

        
 










