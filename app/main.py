import os
import asyncio
from flask import Flask, request, jsonify, render_template, request, session
from telethon import TelegramClient, sync

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_id = os.environ["TELEGRAM_API_ID"]
api_hash = os.environ["TELEGRAM_API_HASH"]
phone = "+34634454832"
username = "@elvesipeto"

# Creating a Flask app object
app = Flask(__name__)
app.secret_key = '12345'  # Change this to a secure random key

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

    # Telegram client
    client = TelegramClient('session_id', api_id, api_hash)
    
    async with client:
        # Ensure you're authorized
        if not await client.is_user_authorized():
            client.send_code_request(phone)
            try:
                client.sign_in(phone, input('Enter the code: '))
            except Exception as e:
                # client.sign_in(password=input('Password: '))
                print("cannot log")
                raise e
            
        print("fetching data for ", input_channel)
        async for msg in client.iter_messages(request.args.get('inputValue'), n):
            messages.append(msg)

    return messages


@app.route('/get_data', methods=['GET'])
async def get_data():
    n = 10
    input_channel = request.args.get('inputValue')
    foo = await get_messages(input_channel, n)
    print("telethon working...", foo)
    await asyncio.sleep(0.1)
    return jsonify("ok")

@app.route('/login', methods=['GET'])
async def login():
    phone_number = request.args.get('phoneNumber')
    client = TelegramClient('session_id', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            session['phone_number'] = phone_number
            return jsonify({"success": True})
        except Exception as e:
            print("An error ocurred", e)
            return jsonify({"success": False})
        
@app.route('/apply_code', methods=['GET'])
async def apply_code(code):
    client = TelegramClient('session_id', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.sign_in(session['phone_number'], code)
            return jsonify({"success": True})
        except Exception as e:
            print("cannot log", e)
            return jsonify({"success": False})
    
    
@app.route('/logout')
def logout():
    session.pop('phone_number', None)
    return jsonify({'success': True})



if __name__ == "__main__":
    app.run(debug=True)