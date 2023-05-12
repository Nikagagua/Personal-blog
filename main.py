import os

from flask import Flask, render_template, request
from datetime import datetime
import requests
import smtplib
from dotenv import load_dotenv

load_dotenv('.env')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

posts = requests.get("https://api.npoint.io/0bd32f974ed7a1c26000").json()
year = datetime.now().year
date = datetime.now().day
app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts, year=year)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post, date=date)


def send_email():
    data = request.form
    name = data['name']
    email = data['email']
    phone = data['phone']
    message = data['message']
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=email,
            to_addrs=EMAIL,
            msg=f"Subject: Message from {name}\n\n"
                f"Name: {name},\n"
                f"Email: {email},\n"
                f"Phone: {phone},\n"
                f"Message: {message}"
        )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template("contact.html", msg_sent=True, send_email=send_email())
    return render_template("contact.html", msg_sent=False)


@app.route("/name-card")
def name_card():
    return render_template("name-card.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
