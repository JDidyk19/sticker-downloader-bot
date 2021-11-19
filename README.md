![](https://img.buzzfeed.com/buzzfeed-static/static/2018-01/24/16/asset/buzzfeed-prod-fastlane-01/sub-buzz-6599-1516828086-2.jpg?downsize=1040%3A%2A&output-quality=auto&output-format=auto)
Sticker Downloader bot
===
**Sticker Downloader Bot** is a Telegram Bot written in Python for downloading telegram stickers.
- [Bot Link](https://t.me/sticker_d0wnl0ader_bot)

Generating an Access Token
===
To make it work, you'll need an access `TOKEN` (it should look something like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
If you don't have it, you have to talk to [@BotFather](https://telegram.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#6-botfather)).

Getting Started
===
To get a local copy up and running follow these simple example steps.

### Installation
- Clone the repo
`git@github.com:JDidyk19/sticker-downloader-bot.git`
- Set your token to the environment variables 
  + On Linux/MAC OS terminal `export TOKEN='your token'`
  + On Windows 10 Command LIne `set TOKEN=your token`
- `cd sticker-downloader-bot/bot`
- Execute the command `pip3 install -r requirements.txt`
- Start app `python3 main.py`

Hosting telegram bot on [Heroku](https://www.heroku.com/) for free
===
Easy way to host your python telegram bot on Heroku.
### Deploying via [Heroku Dashboard](https://dashboard.heroku.com/apps)
- If you don't have an account, you need to create a Heroku account [here](https://signup.heroku.com/login).
- Go to [Dashboard](https://dashboard.heroku.com/apps), Press New and choose Create new app.
- Fill in an **App Name** and choose **Runtime Region**.
- Connect your **GitHub repo** at **Deploy page**.
- Setup Automatics deploys (Optionaly).
- Deploy a GitHub branch.
- Then go to a **Settings page**, click **Reveal Config Vars** and then add your `TOKEN`:
- Finally, go to the **Resources page.**
  + Install **Heroku Redis add-on (Optionaly)**.
  + Press on a small pen button, move slider and then click **Confirm**, that will start bot dyno.
  + Simply move slider back if you need to stop bot dyno, remember to click Confirm.
  + If for some reason it’s not working, check the logs here

  ![](https://camo.githubusercontent.com/e561ede3fcf4c9f88115a4bea7fc2e3d517e24f8ae4215fc9accac3113f52eb8/687474703a2f2f692e696d6775722e636f6d2f72494855367a462e706e67)
