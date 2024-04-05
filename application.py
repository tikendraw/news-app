import sqlite3
from flask import Flask, render_template
from src.prediction import PredictionPipeline  # Import your pipeline class

app = Flask(__name__)

pipeline = PredictionPipeline()  # Initiate the pipeline


@app.route("/")
def index():
    return render_template("index.html")  # Render the HTML template


@app.route("/summarize", methods=["POST"])
def summarize():
    # Connect to the articles.db database file
    conn = sqlite3.connect("articles.db")
    cursor = conn.cursor()

    # Fetch all articles from the database
    cursor.execute(
        "SELECT title, content FROM news_articles WHERE content IS NOT NULL"
    )  # Replace 'news_articles' with your actual table name
    articles = cursor.fetchall()

    article_summaries = []
    for article_title, article_content in articles:
        if article_content is not None:  # Check if content is not null
            summary = pipeline.predict(article_content)
            article_summaries.append({"title": article_title, "summary": summary})
        else:
            # Handle articles with missing content (e.g., display a message)
            article_summaries.append(
                {"title": article_title, "summary": "Summary unavailable"}
            )

    conn.close()  # Close the database connection

    return render_template("result.html", article_summaries=article_summaries)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
