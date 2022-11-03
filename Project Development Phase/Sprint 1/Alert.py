from twilio.rest import Client
from datetime import datetime
import os
from playsound import playsound
from dotenv import load_dotenv
load_dotenv('.env')

account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN')
From = os.getenv('FROM_NUMBER')
To = os.getenv('TO_NUMBER')

def send_alert(Body:str = 'There is Fire!!', To:int = To) -> None :
    '''
    To Ring The Alarm if the  Fire Detected.
    Only Verified twilio numbers can Receive SMS in trail Account.
    
    Body is For MESSAGE CONTENT default is "There is Fire!!"
    To is for RECEIVER_NUMBER default is "env variable"
    
    Change The Defaut value is .env File
    Alert will rang for one Minute Approximately
    '''
    try:
        client = Client(account_sid, auth_token)  
        message = client.messages.create(
                                    from_= From,
                                    body = Body,
                                    to = To
                                    )
    except:
        message = "Something Went Wrong.Message Not Sent! \nCheck, Is your number verified on twilio"
    else:
        message = 'Message Sent!!'
    finally:
        print(message)
        with open('Log.txt','a') as f:
            f.write(f'{datetime.now()} :  There is Fire!!, {message}\n')
            
        # To Ring The alert for One Minute Approximately whether SMS  is sent or Not
        playsound(r'Files\Fire Alarm.mp3')
        
        

if __name__=='__main__':
    send_alert(To='+918667781558')