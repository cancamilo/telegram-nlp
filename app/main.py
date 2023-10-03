import base64
import os
import sys
import platform
import torch
from dotenv import load_dotenv, find_dotenv
from quart import Quart, session, render_template, request, redirect, jsonify
from telethon import TelegramClient, utils
from telethon.errors import SessionPasswordNeededError
from transformers import AutoModelForSequenceClassification

load_dotenv(find_dotenv())

def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)


PHONE_FORM = """
<form action='/' method='post'>
    <h1 class="form-title">Login to telegram</h1>
    <div class="form-group">
    <label for="phone">Phone number:</label>
    <input type="phone" id="phone" name="phone" required>
    </div>
    <div class="form-group">
    <button type="submit">Submit</button>
    </div>
</form>
"""

CODE_FORM = """
<form action='/' method='post'>
    <h1 class="form-title">Login to telegram</h1>
    <div class="form-group">
    <label for="code">Telegram code:</label>
    <input type="text" id="code" name="code" required>
    </div>
    <div class="form-group">
    <button type="submit">Submit</button>
    </div>
</form>
"""

PASSWORD_FORM = """
<form action='/' method='post'>
    Telegram password: <input name='password' type='text' placeholder='your password'>
    <input type='submit'>
</form>
"""

# Session name, API ID and hash to use; loaded from environmental variables
SESSION = os.environ.get("TG_SESSION", "quart")
API_ID = int(get_env("TELEGRAM_API_ID", "Enter your API ID: "))
API_HASH = get_env("TELEGRAM_API_HASH", "Enter your API hash: ")

# Telethon client
# client = TelegramClient("s1", API_ID, API_HASH)
# client.parse_mode = 'html'  # <- Render things nicely
# phone = None

# Quart app
app = Quart(__name__)
app.secret_key = "secret"


# Helper method to format messages nicely
async def format_message(message):
    if message.photo:
        content = '<img src="data:image/png;base64,{}" alt="{}" />'.format(
            base64.b64encode(await message.download_media(bytes)).decode(),
            message.raw_text,
        )
    else:
        # client.parse_mode = 'html', so bold etc. will work!
        content = (message.text or "(action message)").replace("\n", "<br>")

    return "<p><strong>{}</strong>: {}<sub>{}</sub></p>".format(
        utils.get_display_name(message.sender), content, message.date
    )


# Connect the client before we start serving with Quart
# @app.before_serving
# async def startup():
#     # After connecting, the client will create additional asyncio tasks that run until it's disconnected again.
#     # Be careful to not mix different asyncio loops during a client's lifetime, or things won't work properly!
#     print("connecting client", client.api_id)
#     await client.connect()
#     print("client connected")


# After we're done serving (near shutdown), clean up the client
@app.after_serving
async def cleanup():
    # TODO: Disconnect all clients
    # await client.disconnect()
    print("service stopped")


# @app.route("/")
# async def index():
#     return await render_template("login_template.html", content=PHONE_FORM)

sessions_path = "sessions_data"
clients = {}


async def find_client(phone):
    client = clients.get(
        phone, TelegramClient(f"{sessions_path}/{phone}", API_ID, API_HASH)
    )
    await client.connect()
    clients[phone] = client
    return client

async def remove_client(phone):
    client = clients.get(
        phone, TelegramClient(f"{sessions_path}/{phone}", API_ID, API_HASH)
    )    
    await client.connect()
    await client.log_out()
    clients[phone] = None

@app.route("/logout", methods=["GET"])
async def logout():
    print("logging out")
    
    phone_number = session.pop("phone", None)
    if phone_number is not None:
        try:
            await remove_client(phone_number)
            return await render_template("form_frame.html", content=PHONE_FORM)
        except Exception as e:
            print(f"Unable to logout client {phone_number}", e)
            return redirect("/")
    else:
        print("Already logged out")
        return redirect("/")

@app.route("/", methods=["GET", "POST"])
async def root():
    if request.method == "GET":
        # check module versions
        check_versions()
        # Check client
        if not session.get("phone"):
            return await render_template("form_frame.html", content=PHONE_FORM)

        # Retrieve client
        phone = session.get("phone")
        client = await find_client(phone)

        if await client.is_user_authorized():
            # They are logged in, show them some messages from their first dialog
            dialog = (await client.get_dialogs())[0]
            result = "<h1>{}</h1>".format(dialog.title)
            async for m in client.iter_messages(dialog, 10):
                result += await format_message(m)

            return await render_template("inference_frame.html", content="empty")
        else:
            # Redirect to login ?
            return await render_template("form_frame.html", content=PHONE_FORM)

    if request.method == "POST":
        form = await request.form
        if "phone" in form:
            phone = form["phone"]
            print("got phone in form", phone)
            new_client = await find_client(phone)
            await new_client.send_code_request(phone)
            session["phone"] = phone
            return await render_template("form_frame.html", content=CODE_FORM)

        if "code" in form:
            print("code submited...signing in")
            phone = session.get("phone")
            client = await find_client(phone)
            await client.sign_in(code=form["code"])
            return redirect("/")

        # Form not filled, rendering login form again
        print("Empty form")
        return await render_template("form_frame.html", content=result)

@app.route("/get_messages", methods=["GET"])
async def get_messages():
    from predictor import Predictor

    messages = []

    input_channel = str(request.args.get("channel_id"))
    n_messages = int(request.args.get("n"))

    print("input channel", input_channel)
    print("n_messages", n_messages)

    phone = session["phone"]
    if phone is None:
        return jsonify({"success": False})    
    
    print("fetching client...")
    client = await find_client(phone)    
    
    async with client:
        # Ensure you're authorized
        if not await client.is_user_authorized():
            raise Exception("Client not auhtorized")
            
        print("fetching data for ", input_channel)
        try:
            async for msg in client.iter_messages(input_channel, 10):
                messages.append(msg.message)

            filtered_messages = [m for m in messages if m != None and len(m) > 2]
            pred = Predictor()
            result = pred.compute_predictions(filtered_messages)
            print(result)
            return jsonify({"success": True, "messages": messages})
        except Exception as e:
            print(f"Cannot get all messages for {input_channel}", e)
            return jsonify({"success": False, "messages": messages})

def check_versions():
    has_gpu = torch.cuda.is_available()
    has_mps = getattr(torch,'has_mps',False)
    device = "mps" if getattr(torch,'has_mps',False) \
        else "gpu" if torch.cuda.is_available() else "cpu"

    print(f"Python Platform: {platform.platform()}")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"Python {sys.version}")
    print("GPU is", "available" if has_gpu else "NOT AVAILABLE")
    print("MPS (Apple Metal) is", "AVAILABLE" if has_mps else "NOT AVAILABLE")
    print(f"Target device is {device}")

if __name__ == "__main__":
    app.run(debug=True)
