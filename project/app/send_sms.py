# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

def sendAlert(parameter = 'Temperature'):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC8b8154eb7fbedaf4dd7243edb44fb779'
    auth_token = 'd742ad3e37860d0d3709083af8890f95'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='Alert: ' + parameter + ' is surpass critical value! Please take action!',
            from_='+14432666413',
            to='+658427647'
        )

    print(message.sid)