import pandas as pd
import pyodbc
import time
from datetime import date, timedelta, datetime
from dateutil import parser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import sys



db = pyodbc.connect('Driver={SQL Server};', server='localhost', database='RedditData', trusted_connection='yes')
cursor = db.cursor()


def sqlquery(q):
    cursor.execute(q)
    rows = cursor.fetchall()
    return rows


def preprocess_text(text):
    # Tokenize the text]
    if text is None:
        return None
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


def get_sentiment(text):
    if text is None:
        return 0
    scores = analyzer.polarity_scores(text)
    return scores['compound']


analyzer = SentimentIntensityAnalyzer()

startDate = parser.parse("2016-09-19")
endDate = parser.parse(sqlquery("SELECT Max(CreatedAtUtc) FROM RedditData.dbo.Posts")[0][0])

delta = endDate - startDate

for i in range(delta.days + 1):
    firstDay = startDate + timedelta(days=i)
    secondDay = startDate + timedelta(days=i + 1)
    postQuery = "SELECT PostId, PostTitle, selftext, CreatedAtUtc from Posts where CreatedAtUtc >= '" + firstDay.strftime(
        "%Y-%m-%d") + "' AND CreatedAtUtc <= '" + secondDay.strftime("%Y-%m-%d") + "'"
    posts = pd.read_sql(postQuery, db)

    if posts.empty:
        continue

    posts['titleSentiment'] = posts['PostTitle'].apply(get_sentiment)

    if posts['selftext'] is not None:
        posts['cleanText'] = posts['selftext'].apply(preprocess_text)
        posts['bodySentiment'] = posts['cleanText'].apply(get_sentiment)

    for index, post in posts.iterrows():

        commentQuery = "SELECT body, created_utc FROM RedditData.dbo.Comments WHERE post_id = 't3_" + post[
            'PostId'] + "'"
        comments = pd.read_sql(commentQuery, db)
        if comments.empty:
            query = "INSERT INTO RedditData.dbo.SentimentAnalysis (Date, BodySentimentScore, TitleSentimentScore, " \
                    "CommentSentimentScore, PostId) VALUES ('" + firstDay.strftime(
                "%Y-%m-%d") + "', " + str(post['bodySentiment']) + ", " + str(post['titleSentiment']) + ", " + str(0) + ", '" + post['PostId'] + "')"
            cursor.execute(query)
            db.commit()
            continue

        if comments['body'] is not None:
            comments['cleanText'] = comments['body'].apply(preprocess_text)
            comments['sentiment'] = comments['cleanText'].apply(get_sentiment)
        query = "INSERT INTO RedditData.dbo.SentimentAnalysis (Date, BodySentimentScore, TitleSentimentScore, " \
                "CommentSentimentScore, PostId) VALUES ('" + firstDay.strftime(
            "%Y-%m-%d") + "', " + str(post['bodySentiment']) + ", " + str(post['titleSentiment']) + ", " + str(
            comments['sentiment'].mean()) + ", '" + post['PostId'] + "')"
        cursor.execute(query)
        db.commit()
