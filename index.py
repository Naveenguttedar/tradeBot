from flask import Flask, request
import json
import re
from telegram import Bot

# Define your Telegram bot token
TOKEN = "7106683591:AAF1g1s7apssNPVkoT5IBVajqFkurvwvH5Y"

# Create a Telegram bot instance
bot = Bot(TOKEN)

# Function to decode message
def decode_msg(text):
    cleaned_text = text.replace('\n', '')
    print("cleaned text ",cleaned_text)
    regex = r'Currency pair\s*([\w/]+)\s*.*put\s*["\']?(UP|DOWN)["\']?'
    match = re.search(regex, cleaned_text)
    if match:
        currency_pair = match.group(1)  # EUR/USD
        put_option = match.group(2)      # UP or DOWN
        return f"Currency Pair: {currency_pair}\nPut Option: {put_option}"
    else:
        return "No match found."

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
async def webhook():
    # Check if the request contains JSON data
    if request.is_json:
        # Get the JSON data
        data = request.get_json()
        message=data.get('message',' ')       # Do something with the received data and decoded message
        chat_id = message['chat']['id']
        caption=message.get('caption','caption not found ')
        signal = decode_msg(caption)
        try:
            # Send message
            await bot.send_message(chat_id, signal)
            print("Message sent successfully")
            return {"message": "Received POST request successfully"}, 200
        except Exception as e:
            print("Error:", e)
            return {"error": "Failed to send message"}, 500 
        # Respond with a success message
        return {"message": "Received POST request successfully"}, 200
    else:
        # If the request does not contain JSON data, respond with an error
        return {"error": "Request must contain JSON data"}, 400

if __name__ == '__main__':
    app.run(debug=True)

