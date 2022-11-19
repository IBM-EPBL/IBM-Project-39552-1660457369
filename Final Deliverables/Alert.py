from twilio.rest import Client, TwilioException
from datetime import datetime
import os
from playsound import playsound
from dotenv import load_dotenv
load_dotenv('.env')

account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN')
From = os.getenv('FROM_NUMBER')
To = os.getenv('TO_NUMBER')

client = Client(account_sid, auth_token)


def is_valid_number(number):
    try:
        response = client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioException as e:
            return False



def send_alert(Body:str = 'There is Fire!!', To:int = To) -> None :
    '''
    To Ring The Alarm if the  Fire Detected.
    Only Verified twilio numbers can Receive SMS in trail Account.
    
    Body is For MESSAGE CONTENT default is "There is Fire!!"
    To is for RECEIVER_NUMBER default is "env variable"
    
    Change The Defaut value is .env File
    Alert will rang for one Minute Approximately
    '''
    if not is_valid_number(To):
        print('Enter a valid Twilio Verified Number')
        exit(0)
    
    try:  
        message = client.messages.create(
                                    from_= From,
                                    body = Body,
                                    to = To
                                    )
    except:
        message = "Your Number is not Registered in Twilio.Message Not Sent!!"
    else:
        message = 'Message Sent!!'
    finally:
        print(message)
        with open('Log.txt','a') as f:
            f.write(f'{datetime.utcnow()} :  There is Fire!!, {message} To {To}\n')
            
        # To Ring The alert for One Minute Approximately whether SMS  is sent or Not
        playsound('Files/Fire Alarm.mp3')
        
        

if __name__=='__main__':
    send_alert(To='+918667781558')