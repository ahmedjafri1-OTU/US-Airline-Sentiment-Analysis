import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import STOPWORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.title("Sentiment Analysis of Tweets of US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets of US Airlines")
st.markdown(" A dashboard powered by Streamlit to analyze the sentiment of tweets related to US Airlines  ")

# Load the dataset

@st.cache_data
def load_data():
    data = pd.read_csv("Tweets.csv")
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))

#query data frame 
# return is a data frame, sample one row, and get the text column value
# return to dataframe and get the text column value
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment") 
select = st.sidebar.selectbox("Visualization type", ["Histogram", "Pie chart"], key="1")

sentiment_count = data["airline_sentiment"].value_counts()
# convert to data frame
# create a data frame with two columns, sentiment and count
# sentiment_count.index is the sentiment, sentiment_count.values is the count
sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index, "Tweets": sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Sentiment", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, names="Sentiment", values="Tweets", color="Sentiment")
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are the tweets?")
hour=st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data["tweet_created"].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key="2"):
    st.markdown("### Tweets location based on the hour of the day")
    # st.markdown("### Tweets location based on the hour of the day")
    # len(modified_data) is the number of tweets in the modified data frame, hour is the selected hour, (hour+1)%24 is the next hour
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    # group by location and count the number of tweets in each location, reset the index, and rename the columns
    st.map(modified_data)
    # create a scatter geo plot with location as the location, size as the number of tweets, and scope as USA
    if st.sidebar.checkbox("Show Plot", False, key="3"):
        st.write(modified_data)


st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"), key="4")

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count", color="airline_sentiment", facet_col="airline_sentiment", labels={"airline_sentiment": "Tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.subheader("Word Cloud")
word_sentiment=st.sidebar.radio("Display word cloud Sentiment", ("positive", "neutral", "negative"), key="5")

if not st.sidebar.checkbox("Hide", True, key="6"):
    st.header("Word cloud for %s sentiment" % (word_sentiment))
    df = data[data["airline_sentiment"] == word_sentiment]
    words = " ".join(df["text"])
    processed_words = " ".join([word for word in words.split() if 'http' not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot()


