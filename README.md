# SI106_FinalProject_SentimentAnalysis_Twitter_NYT_API

Final Project – README Template
I. Type of project (delete those that do not apply): 

1) API project


II. Brief description of project:
Searches 100 tweets from Twitter and 10 most recent headlines from The New York Times with “Trump” in the tweet or headline. Calculates the emo score of each tweet/headline. Creates 2 CSV files of all of the emo scores for each tweet/headline. The CSV files also include at the bottom how many positive, negative, and neutral tweets/headlines there were, the top(most frequent) emo score, and the mean emo score. It additionally prints out for the user whether there were more positive, negative, or neutral tweets/headlines and the most frequent and mean emo score. 


III. List of files being turned in, with a brief description of each one:
negative-words.txt - file of negative words for conducting emo score
positive-words.txt - file of positive words for conducting emo score 
test106.py - test file for test cases 
Halbeisen.py - main project file 
project_README_template.txt - this file 

IV. Python packages/modules that need to be installed (e.g. BeautifulSoup):
import requests_oathlib
import requests
import webbrowser
import json
import test106 as test 

V. Instructions for running/using/playing project:
python Halbeisen.py


VI. Data sources used (for API projects only):
Twitter API 
New York Times Article Search API 

VII. Approximate line numbers in main python file to find following components (if they occur in another code file, note this):

Accumulation pattern
# 181-186, 293-298

Sort with a key function	
# 188, 300

Class definition
# 83, 211
__init__() method for this class	
85-93, 213-219
First method for this class	
95-100, 222-227
Second method for this class	
102-107, 229-234
Importation of a python module, either built-in or third-party	
2
Use of this module in the code:	
207

Use of list comprehension OR map OR filter	
157, 161, 165 

Definitions of 5 functions or methods (can include class methods above)	
# 1 	class Post which has methods positive, negative, and emo_score 
# 2 	function keep_positive 
# 3 	function keep_negative 
# 4 	function keep_neutral 
# 5 	class Score which has methods positive, negative, and emo_score 

Test cases for at least three functions or methods	
# 1 126-133
# 2 142-148
# 3 153-260


VIII. Rationale for project; why did you do this project? Why do you find it interesting?
I did this project because I wanted to be able to gauge public opinion of a presidential candidate in comparison with a popular news source. What I found most interesting was some of the tweets/headlines I got back from my requests. It was pretty entertaining at times. Also, I realized after completing my project that finding emo scores aren’t that accurate at indicating whether something is positive or negative. For example, the headline “Ted Cruz Surges Past Donald Trump to Lead in Iowa Poll” is a negative headline about Trump, but my program indicates it as a positive one. So that finding was pretty interesting as all semester we have been talking about computers vs humans. Just like the dance example in class, computers take everything literally and do only and exactly what you tell it to do. I truly understand how significant that fact is now that I have spent hours writing a program that actually isn’t very meaningful. 
