from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import EmailStr
from jinja2 import Template


from datetime import datetime

app = FastAPI()

subscriptions = dict()

page = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    {{ content }}
</body>
</html>"""

form = """
    <form action="{{ action }}" method="POST">
        <div>
            <label for="email">Your email: </label>
            <input type="email" name="email" id="email" />
        </div>
        <div>
            <button>{{ button_text }}</button>
        </div>
    </form>
    <div>
        {{ footer }}
    </div>
"""


@app.get("/", response_class=HTMLResponse)
async def root():
    rendered_form = Template(form).render(
        {
            "action": "/subscribe",
            "button_text": "Sign me up!",
            "footer": 'To unsubscribe go <a href="/unsubscribe/">here.</a>',
        }
    )
    return Template(page).render(
        {
            "title": "Sign me up!",
            "heading": "Subscribe now :)",
            "content": rendered_form,
        }
    )


@app.get("/unsubscribe/", response_class=HTMLResponse)
async def unsubscribe():
    rendered_form = Template(form).render(
        {
            "action": "/unsubscribe",
            "button_text": "Unsubscribe",
            "footer": 'To subscribe go <a href="/">here.</a>',
        }
    )
    return Template(page).render(
        {
            "title": "Unsubscribe :(",
            "heading": "Subscribe now :)",
            "content": rendered_form,
        }
    )


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(email: EmailStr = Form(default=None)):
    if not email:
        return Template(page).render(
            {
                "title": "Subscription Failure",
                "heading": "Subscription failed:",
                "content": "You did not provide a valid email.",
            }
        )
    if email not in subscriptions:
        subscriptions[email] = datetime.now()
    return Template(page).render(
        {
            "title": "Subscription successful!",
            "heading": "Successfully subscribed!",
            "content": "",
        }
    )


@app.post("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(email: EmailStr = Form(default=None)):
    if not email:
        return Template(page).render(
            {
                "title": "Removing subscription failed",
                "heading": "Removing subscription failed:",
                "content": "You did not provide a valid email.",
            }
        )
    if email in subscriptions:
        del subscriptions[email]
    return Template(page).render(
        {
            "title": "Unsubscripted successfully!",
            "heading": "Unsubscribed, we will miss you!",
            "content": "",
        }
    )


table = """
<table>
    <tr>
        <th>eMail</th>
        <th>Date Joined</th>
    </tr>
    {% for email, date_joined in subscriptions.items() %}
    <tr>
        <th>{{email}}</th>
        <th>{{date_joined}}</th>
    </tr>
    {% endfor %}
</table>
"""


@app.get("/list_subscriptions/", response_class=HTMLResponse)
async def list_subscriptions():
    rendered_table = Template(table).render({"subscriptions": subscriptions})
    return Template(page).render(
        {
            "title": "Sign me up!",
            "heading": "List of Subscriptions",
            "content": rendered_table,
        }
    )
