from flask import Flask, render_template
from ..db.crud.news_crud import NewsArticleSummaryRepository
from ..db.db_utils import get_db
from ..schema.article_summary import ShowArticleSummary
from icecream import ic

# ic.disable()
ic.enable()

app = Flask(__name__)


news_repo = NewsArticleSummaryRepository()
db_session = next(get_db())


@app.route("/")
def index():
    instruction = "Go to /test"
    return render_template("index.html", instruction=instruction)


def article_summary_to_json(article_summary: list[ShowArticleSummary]) -> list[dict]:
    return [article_summary.to_json() for article_summary in list]


@app.route("/test")
def test_index():  # sourcery skip: identity-comprehension
    # news_articles = news_repo.get_by_id(obj_id=1, db=db_session, response_model=ShowArticleSummary, return_dict=True)
    # news_articles = news_repo.get_n(db=db_session, n=3, response_model=ShowArticleSummary, return_dict=True)
    news_articles = news_repo.get_latest_n(n=10, db=db_session, response_model=ShowArticleSummary, return_dict=True)
    print(len(news_articles))

    return render_template(
        "test.html",
        news_articles=news_articles

    )


if __name__ == "__main__":
    print("Running: ", __file__)
