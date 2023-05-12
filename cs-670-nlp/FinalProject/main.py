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
import io
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

startDate = parser.parse("2017-04-28")
endDate = parser.parse(sqlquery("SELECT Max(CreatedAtUtc) FROM RedditData.dbo.Posts")[0][0])

delta = endDate - startDate

for i in range(delta.days + 1):
    firstDay = startDate + timedelta(days=i)
    secondDay = startDate + timedelta(days=i + 1)
    postQuery = f"SELECT PostId, PostTitle, selftext, CreatedAtUtc from Posts where CreatedAtUtc >= '{firstDay.strftime('%Y-%m-%d')}' AND CreatedAtUtc < '{secondDay.strftime('%Y-%m-%d')}'"
    posts = pd.read_sql(postQuery, db)

    if posts.empty:
        continue

    posts['titleSentiment'] = posts['PostTitle'].apply(get_sentiment)

    if posts['selftext'] is not None:
        posts['cleanText'] = posts['selftext'].apply(preprocess_text)
        posts['bodySentiment'] = posts['cleanText'].apply(get_sentiment)

    postString = ''
    for p in posts['PostId']:
        postString += '\'t3_' +p + '\','

    commentQuery = f"SELECT body, created_utc, post_id FROM RedditData.dbo.Comments WHERE post_id in ({postString.rstrip(postString[-1])})"

    allComments = pd.read_sql(commentQuery, db)

    values = ""
    for index, post in posts.iterrows():

        comments = allComments[allComments['post_id'] == 't3_' + post['PostId']]
        if comments.empty:
            values += f"('{firstDay.strftime('%Y-%m-%d')}', {post['bodySentiment']}, {post['titleSentiment']}, {0}, 't3_{post['PostId']}'),"
            continue

        if comments['body'] is not None:
            comments['cleanText'] = comments['body'].apply(preprocess_text)
            comments['sentiment'] = comments['cleanText'].apply(get_sentiment)
        values += f"('{firstDay.strftime('%Y-%m-%d')}', {post['bodySentiment']}, {post['titleSentiment']}, {comments['sentiment'].mean()}, 't3_{post['PostId']}'),"

    query = f"INSERT INTO RedditData.dbo.SentimentAnalysis (Date, BodySentimentScore, TitleSentimentScore, CommentSentimentScore, PostId) VALUES {values.rstrip(postString[-1])}"
    cursor.execute(query)
    db.commit()
