import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai_handler import analyze_intent
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get message details from Twilio webhook
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        print(f"Received message from {from_number}: {incoming_msg}")
        
        # Process with AI
        response_text = analyze_intent(from_number, incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        return str(resp), 200
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, something went wrong. Please try again.")
        return str(resp), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
