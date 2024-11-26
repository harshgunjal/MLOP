import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Configure the Streamlit page
st.set_page_config(page_title="Advanced Sentiment Analysis", page_icon="😊", layout="wide")

# App title and description
st.title("😊 Advanced Sentiment Analysis App")
st.write("Analyze the sentiment of your text in real-time! See a breakdown of sentiment polarity, subjectivity, and visualize your words.")

# Create columns for layout
col1, col2 = st.columns(2)

# Sentiment history to display previous results
if "sentiment_history" not in st.session_state:
    st.session_state["sentiment_history"] = []

# Helper function for sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

# Display sentiment emoji based on polarity score
def sentiment_emoji(polarity):
    if polarity > 0.1:
        return "😊 Positive"
    elif polarity < -0.1:
        return "😞 Negative"
    else:
        return "😐 Neutral"

# Generate a word cloud image
def generate_wordcloud(text):
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text)
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Sidebar for additional options and example text
with st.sidebar:
    st.subheader("Options")
    example_text = st.selectbox(
        "Or select an example text:",
        ["", "I love this product! It's amazing and works perfectly.", 
         "I'm not happy with the service; it was slow and unhelpful.", 
         "It's an okay experience, nothing special."]
    )
    show_wordcloud = st.checkbox("Show Word Cloud", value=True)
    real_time_analysis = st.checkbox("Enable Real-Time Analysis", value=True)

# Main text input
with col1:
    st.subheader("Enter Text for Sentiment Analysis")
    user_text = st.text_area("Type or paste text here:", example_text)

    # Real-time or on-demand analysis
    if real_time_analysis or st.button("Analyze Sentiment"):
        if user_text.strip():
            # Analyze sentiment
            polarity, subjectivity = analyze_sentiment(user_text)
            emoji = sentiment_emoji(polarity)
            st.write(f"**Sentiment**: {emoji}")
            st.write(f"**Polarity Score**: {polarity:.2f}")
            st.write(f"**Subjectivity Score**: {subjectivity:.2f}")

            # Display a horizontal bar graph of sentiment
            st.write("#### Sentiment Graph")
            st.progress((polarity + 1) / 2)  # Scale polarity to [0,1] for progress bar

            # Store sentiment analysis in history
            st.session_state["sentiment_history"].append({
                "Text": user_text[:50] + "..." if len(user_text) > 50 else user_text,
                "Sentiment": emoji,
                "Polarity": polarity,
                "Subjectivity": subjectivity
            })

        else:
            st.warning("Please enter some text for analysis.")

# Display word cloud in the second column if enabled
with col2:
    st.subheader("Sentiment Visualization")
    if show_wordcloud and user_text.strip():
        generate_wordcloud(user_text)
    else:
        st.info("Enable the word cloud option to visualize word prominence.")

# Display sentiment history
st.write("---")
st.subheader("Sentiment Analysis History")
if st.session_state["sentiment_history"]:
    history_df = pd.DataFrame(st.session_state["sentiment_history"])
    st.dataframe(history_df)
else:
    st.write("No sentiment history yet.")

# Additional notes on analysis
st.write("---")
st.write("**Note**: Polarity ranges from -1 to 1, where values closer to 1 indicate positive sentiment, values closer to -1 indicate negative sentiment, and values near 0 indicate neutral sentiment. Subjectivity ranges from 0 (objective) to 1 (subjective).")
