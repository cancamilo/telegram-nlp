import os
import asyncio
from flask import Flask, request, jsonify, render_template
from telethon import TelegramClient, sync

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_id = os.environ["TELEGRAM_API_ID"]
api_hash = os.environ["TELEGRAM_API_HASH"]
phone = "+34634454832"
username = "@elvesipeto"

# Telegram client
client = TelegramClient('session_id', api_id, api_hash)

# Get event loop
loop = client.loop

# Creating a Flask app object
app = Flask(__name__)

# Defining the route for the index page
@app.route("/test", methods=["GET", "POST"])
def test():
    print("hello human")
    return jsonify({"inference": "positive!!"})

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

async def get_messages(input_channel: str, n: int):
    messages = []
    client = TelegramClient('session_id', api_id, api_hash)
    await client.start()

    # # Ensure you're authorized
    # if not await client.is_user_authorized():
    #     client.send_code_request(phone)
    #     try:
    #         client.sign_in(phone, input('Enter the code: '))
    #     except Exception as e:
    #         # client.sign_in(password=input('Password: '))
    #         print("cannot log")
    #         raise e
        
    print("fetching data for ", input_channel)
    async for msg in client.iter_messages(request.args.get('inputValue'), n):
        messages.append(msg)

    return messages


@app.route('/get_data', methods=['GET'])
async def get_data():
    n = 10
    input_channel = request.args.get('inputValue')
    print("gettin data...")
    foo = await get_messages(input_channel, n)
    print("telethon working...", foo)

    await asyncio.sleep(0.5)
    print("loop worked")
    return jsonify(foo)

if __name__ == "__main__":
    loop.run_until_complete(app.run(debug=True))