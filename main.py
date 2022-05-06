from datetime import date, datetime
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

debug_mode = False

app = Flask(__name__)
app.secret_key = 'super-secret-key'

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

print(params['gmail-user'])
print(params['gmail-password'])


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)

def send_mail(contact_name, contact_title, contact_email, contact_message):
    try:
        mail.send_message('New message from ' + contact_name,
                    sender=contact_email,
                    recipients = [params['gmail-user']],
                          body = contact_title + "\n" + contact_message
                          )


        print("Successfuly sent")
    except Exception as e:
        print(f"Exception is {e}")


@app.route("/")
def home():
    discord_server_link = params['discord-server-link']
    return render_template("index.html", discord_server_link=discord_server_link)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    discord_server_link = params['discord-server-link']
    if request.method == "POST":
        contact_name = request.form.get("contact_name")
        contact_title = request.form.get("contact_title")
        contact_message = request.form.get("contact_message")
        contact_email = request.form.get("contact_email")

        send_mail(contact_name, contact_title, contact_message, contact_email)

    return render_template("contact.html", discord_server_link=discord_server_link)

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/services")
def services():
    return render_template("services.html")

if __name__ == "__main__":
    app.run(debug=debug_mode, host='0.0.0.0.')