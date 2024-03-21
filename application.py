from flask import Flask, request, render_template
from src.core.pipeline.prediction import PredictionPipeline  # Import your pipeline class

app = Flask(__name__)

pipeline = PredictionPipeline()  # Instantiate the pipeline

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    summary = pipeline.predict(text)
    return render_template('result.html', summary=summary)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
