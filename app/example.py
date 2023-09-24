import base64
import os
from dotenv import load_dotenv, find_dotenv
from quart import Quart, render_template_string, render_template, request
from telethon import TelegramClient, utils
from telethon.errors import SessionPasswordNeededError
import asyncio

load_dotenv(find_dotenv())

def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)

PHONE_FORM = '''
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
'''

CODE_FORM = '''
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
'''

PASSWORD_FORM = '''
<form action='/' method='post'>
    Telegram password: <input name='password' type='text' placeholder='your password'>
    <input type='submit'>
</form>
'''

# Session name, API ID and hash to use; loaded from environmental variables
SESSION = os.environ.get('TG_SESSION', 'quart')
API_ID = int(get_env('TELEGRAM_API_ID', 'Enter your API ID: '))
API_HASH = get_env('TELEGRAM_API_HASH', 'Enter your API hash: ')

# Telethon client
client = TelegramClient("s1", API_ID, API_HASH)
client.parse_mode = 'html'  # <- Render things nicely
phone = None

# Quart app
app = Quart(__name__)
app.secret_key = 'secret'

loop = client.loop

# Helper method to format messages nicely
async def format_message(message):
    if message.photo:
        content = '<img src="data:image/png;base64,{}" alt="{}" />'.format(
            base64.b64encode(await message.download_media(bytes)).decode(),
            message.raw_text
        )
    else:
        # client.parse_mode = 'html', so bold etc. will work!
        content = (message.text or '(action message)').replace('\n', '<br>')

    return '<p><strong>{}</strong>: {}<sub>{}</sub></p>'.format(
        utils.get_display_name(message.sender),
        content,
        message.date
    )


# Connect the client before we start serving with Quart
@app.before_serving
async def startup():
    # After connecting, the client will create additional asyncio tasks that run until it's disconnected again.
    # Be careful to not mix different asyncio loops during a client's lifetime, or things won't work properly!
    print("connecting client", client.api_id)
    await client.connect()
    print("client connected")


# After we're done serving (near shutdown), clean up the client
@app.after_serving
async def cleanup():
    await client.disconnect()

# @app.route("/")
# async def index():
#     return await render_template("login_template.html", content=PHONE_FORM)

@app.route('/', methods=['GET', 'POST'])
async def root():
    # return await render_template("form_frame.html", content=PHONE_FORM)
    
    # We want to update the global phone variable to remember it
    global phone

    # Check form parameters (phone/code)
    form = await request.form
    if 'phone' in form:
        print("phone submited...sending code")
        phone = form['phone']
        await client.send_code_request(phone)

    if 'code' in form:
        print("code submited...signing in")
        try:
            await client.sign_in(code=form['code'])
        except SessionPasswordNeededError:
            return await render_template("form_frame.html", content=PASSWORD_FORM)

    if 'password' in form:
        print("signing in with password")
        await client.sign_in(password=form['password'])

    # If we're logged in, show them some messages from their first dialog
    if await client.is_user_authorized():
        # They are logged in, show them some messages from their first dialog
        dialog = (await client.get_dialogs())[0]
        result = '<h1>{}</h1>'.format(dialog.title)
        async for m in client.iter_messages(dialog, 10):
            result += await(format_message(m))

        return await render_template("form_frame.html", content=result)
    
    # Ask for phone if not available
    if phone is None:
        print("no phone...rendering phone form")
        return await render_template("form_frame.html", content=PHONE_FORM)

    # We have the phone, but we're not logged in, so ask for the code
    print("phone but no code...rendering code form")
    return await render_template("form_frame.html", content=CODE_FORM)

if __name__ == '__main__':    
    app.run(debug=True, loop = loop)