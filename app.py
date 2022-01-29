from quart import Quart, redirect, url_for, render_template
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Quart(__name__)

app.secret_key = b"random bytes representing quart secret key"

app.config["DISCORD_CLIENT_ID"] = 929799004672376902   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "ddxwkQi8I-XodA1N9bXzfYmcdC8RdnJA"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "OTI5Nzk5MDA0NjcyMzc2OTAy.YdskzQ.CA7eG5sIVUJz0V03DzqSWjtpwSs"                    # Required to access BOT resources.


discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    return redirect(url_for(".login"))
@app.route("/login/")
async def login():
    return await discord.create_session(permissions=8)


@app.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
async def me():
    user = await discord.fetch_user()
    return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <link rel="stylesheet" href="style.css">
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Ernold Dashboard</title>
            </head>
            <body>
                <img src="{user.avatar_url}" alt="">
                
                <h1>Willkomen!</h1>
                <p>
                    {user.name}
                </p>
            </body>
            </html>

                    
            """


if __name__ == "__main__":
    app.run()
