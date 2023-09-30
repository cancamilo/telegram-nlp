import os
import asyncio
from quart import Quart, request, jsonify, render_template, request, session
from telethon import TelegramClient

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_id = os.environ["TELEGRAM_API_ID"]
api_hash = os.environ["TELEGRAM_API_HASH"]
phone = "+34634454832"
username = "@elvesipeto"

# Creating a Flask app object
app = Flask(__name__)
app.secret_key = '12345'  # Change this to a secure random key
sessions_path = "sessions_data"

# Telegram client
client = TelegramClient(f"{sessions_path}/{phone}", api_id, api_hash)
loop = client.loop

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

async def async_get_messages(input_channel: str, n: int):
    messages = []
    
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

async def get_messages(input_channel: str, n: int):
    messages = []
    
    await client.connect()
    client.start()

    # Ensure you're authorized
    # if not client.is_user_authorized():
    #     client.send_code_request(phone)
    #     try:
    #         client.sign_in(phone, input('Enter the code: '))
    #     except Exception as e:
    #         # client.sign_in(password=input('Password: '))
    #         print("cannot log")
    #         raise e
            
    #     print("fetching data for ", input_channel)

    # for msg in loop.run_until_complete(client.get_messages(input_channel, n)):
    #     messages.append(msg)

    return messages


@app.route('/get_data', methods=['GET'])
async def get_data():
    n = 5
    input_channel = request.args.get('inputValue')
    print("requesting messages...")
    foo = await get_messages(input_channel, n)
    print("telethon working...", foo)    
    return jsonify("ok")

@app.route('/login', methods=['GET'])
async def login():
    phone_number = request.args.get('phoneNumber')
    client = TelegramClient(f"{sessions_path}/{phone_number}", api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            session['phone_number'] = phone_number
            return jsonify({"success": True})
        except Exception as e:
            print("An error ocurred", e)
            return jsonify({"success": False})
    else:
        return jsonify({"success": True})

        
@app.route('/apply_code', methods=['GET'])
async def apply_code():
    code = request.args.get('code')
    phone_number = session['phone_number']
    client = TelegramClient(f"{sessions_path}/{phone_number}", api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.sign_in(session['phone_number'], code)
            return jsonify({"success": True})
        except Exception as e:
            print("cannot log", e)
            return jsonify({"success": False})
    else:
        return jsonify({"success": True})
    
    
@app.route('/logout')
async def logout():
    phone_number = session.pop('phone_number', None)
    client = TelegramClient(f"{sessions_path}/{phone_number}", api_id, api_hash)
    await client.log_out()
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)