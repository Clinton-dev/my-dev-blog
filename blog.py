from flask import Flask, render_template,url_for

app = Flask(__name__)

blogs = [
    {
        "title":"First blog post",
        "content": "",
        "date_posted":"13-02-2021",
        "no_of_comments":30
    },
    {
        "title":"second blog post",
        "content": "",
        "date_posted":"25-04-2022",
        "no_of_comments":15
    },
    {
        "title":"third blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    },
    {
        "title":"fourth blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    },
    {
        "title":"fifth blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    }
]

@app.route("/")
def hello_world():
    return render_template("index.html", blogs=blogs)

if __name__ == "__main__":
    app.run(debug=True)