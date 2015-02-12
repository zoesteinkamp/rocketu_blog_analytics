import requests

__author__ = 'GKadillak'

def send_mail(user_email):
    return requests.post(
        "https://api.mailgun.net/ec2-54-187-179-27.us-west-2.compute.amazonaws.com/messages",
        auth=("api", "key-aef81e555aef520b14d4641910af2fce"),
        data={"from": "Excited User <gkadillak@gmail.com>",
            "to": [user_email],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!"})
