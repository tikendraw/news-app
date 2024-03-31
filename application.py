from flask import Flask, render_template
from src.prediction import PredictionPipeline  # Import your pipeline class
import json

app = Flask(__name__)

pipeline = PredictionPipeline()  # Intiate the pipeline


@app.route("/")
def index():
    return render_template("index.html")  # Render the HTML template


# @app.route('/summarize', methods=['POST'])
# def summarize():
#     text = request.form['text']
#     summary = pipeline.predict(text)
#     return render_template('result.html', summary=summary)


@app.route("/summarize", methods=["POST"])
def summarize():
    # Load news data from gnews.json
    with open("gnews.json", "r") as f:
        news_data = json.load(f)
    articles = news_data["articles"]

    article_summaries = []
    for article in articles:
        summary = pipeline.predict(article["content"])
        article_summaries.append({"title": article["title"], "summary": summary})

    return render_template("result.html", article_summaries=article_summaries)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
