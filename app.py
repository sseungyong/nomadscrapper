from flask import Flask, render_template, request, redirect, send_file
from nomad_scrapper import nomad_job_scrapper
from save_result import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = nomad_job_scrapper(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html",
        searchingBy=word,
        resultNumber=len(jobs),
        jobs=jobs
    )


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")

# @app.route("/contact")
# def contact():
#     return "Contact me!!"


# @app.route("/<username>")
# def user_home(username):
#     return f"Hi! {username}, How are you doing??"


if __name__ == "__main__":
    app.run()
