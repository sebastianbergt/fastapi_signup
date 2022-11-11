from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import EmailStr

from datetime import datetime

app = FastAPI()

subscriptions = dict()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Sign me up!</title>
</head>
<body>
    <h1>Subscribe now :)</h1>
    <form action="/subscribe" method="POST">
        <div>
            <label for="email">Your email: </label>
            <input type="email" name="email" id="email" />
        </div>
        <div>
            <button>Sign me up!</button>
        </div>
    </form>
    <div>
    To unsubscribe go <a href="/unsubscribe/">here.</a>
    </div>
</body>
</html>
"""


@app.get("/unsubscribe/", response_class=HTMLResponse)
async def unsubscribe():
    return """
<html>
<head>
    <title>Unsubscribe :(</title>
</head>
<body>
    <h1>Unsubscribe</h1>
    <form action="/unsubscribe" method="POST">
        <div>
            <label for="email">Your email: </label>
            <input type="email" name="email" id="email" />
        </div>
        <div>
            <button>Unsubscribe</button>
        </div>
    </form>
    <div>
    To subscribe go <a href="/">here.</a>
    </div>
</body>
</html>
"""


@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe(email: EmailStr = Form(default=None)):
    if not email:
        return "You did not provide a valid email."
    if email not in subscriptions:
        subscriptions[email] = datetime.now()
    return "Successfully subscribed!"


@app.post("/unsubscribe", response_class=HTMLResponse)
async def subscribe(email: EmailStr = Form(default=None)):
    if not email:
        return "You did not provide a valid email."
    if email in subscriptions:
        del subscriptions[email]
    return "Unsubscribed, we will miss you!"


@app.get("/list_subscriptions/", response_class=HTMLResponse)
async def list_subscriptions():

return """
<html>
<head>
    <title>Subscribers</title>
</head>
<body>
    <h1>Subscribers</h1>
    
</body>
</html>
"""

    return {subscriptions}
