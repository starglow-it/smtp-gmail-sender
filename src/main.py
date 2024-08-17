from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json
import time
from itertools import cycle, islice
import socket

from gpt_generate_message import generate_message
from scrape_website import fetch_website_data

# Load environment variables from .env file
load_dotenv()

# OpenAI Client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# MongoDB connection
mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
db = mongo_client['reachStream']

# Email settings
smtp_server = os.getenv('SMTP_SERVER')  
smtp_port = os.getenv('SMTP_PORT') 

def load_smtp_credentials():
    credential_list = []
    index = 1  # Start with credential set 1

    # Loop until no more credential sets are found
    while True:
        smtp_user = os.getenv(f'SMTP_USER_{index}')
        smtp_password = os.getenv(f'SMTP_PASSWORD_{index}')
        user_name = os.getenv(f'SMTP_USERNAME_{index}')

        if smtp_user and smtp_password and user_name:
            credential_list.append({
                'smtp_user': smtp_user,
                'smtp_password': smtp_password,
                'user_name': user_name
            })
            index += 1
        else:
            break # Exit loop
    
    return credential_list

def send_email(server, from_email, to_email, subject, message):
    print('From: ', from_email, '       To: ', to_email)

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))

    #Send the email
    try:
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("Email has been sent successfully.")

        return True
    except smtplib.SMTPConnectError as e:
        print(f"Connection Error, {e}")

        return False
    except smtplib.SMTPSenderRefused as e:
        print('SMTPSenderRefused', {e})
        return False
    except smtplib.SMTPResponseException as e:
        if ('Daily user sending limit exceeded' in str(e.smtp_error)) :
            print('Daily sending limit exceeded. Removing this email address from today\'s sending email list.')

        return 'limit_exceeded'
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

        return False


def fetch_and_parse_gpt_response(openai_client, contact, company_description, user_name):
    max_retries = 5
    retry_delay = 2  # seconds
    for attempt in range(max_retries):
        try:
            # Assuming generate_message is your function that calls the GPT API
            gpt_response = generate_message(openai_client, contact['contact_name'], contact['contact_email_1'], contact['company_company_name'], company_description, user_name)
            # Parse JSON into dictionary
            parsed_response = json.loads(gpt_response)

            return parsed_response  # Successfully parsed, return the response
        except Exception as e:
            print(f"JSON decode error on attempt {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # Wait for a bit before retrying
            else:
                print("Max retries reached. Moving to the next contact.")
                # Handle the failure case, e.g., log error, skip to next contact, etc.
                return None
    

def main():
    # Get collection name, start index and end index from the user input
    collection_name = input('Enter the collection name: ')
    start_index = int(input('Enter the start index: '))
    end_index = int(input('Enter the end index: '))
    time_interval = int(input('Enter the time interval in seconds: '))

    credential_list = load_smtp_credentials()

    contacts_collection = db[collection_name]  # Here, replace the collection name you want to send email to.

    # Cycle through credentials indefinitely
    credential_cycle = cycle(credential_list)

    # Retrieving only filtered data from the database and sort by id.
    contacts = list(contacts_collection.find({'passed_validator': {'$ne': None}}).sort({'id': 1}))[start_index:end_index]

    for index, contact in enumerate(contacts):
        # Check if the credential list is empty
        if not credential_list:
            print('Credential list is empty. Exiting here...')
            break

        print('Sending Email No.', start_index + index, '...')

        cred = next(credential_cycle)

        try:    
            # SMTP Server configuration
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()   # Enable security
            server.login(cred['smtp_user'], cred['smtp_password'])   # Login with credential

            # Scrape company description from their website
            company_description = fetch_website_data(contact['company_website'])

            # Retrieve response dictionary after fetching GPT API and parsing.
            parsed_dict = fetch_and_parse_gpt_response(openai_client, contact, company_description, cred['user_name'])

            # If still error in GPT response and exceed the maximum count, move to the next content
            if (parsed_dict == None):
                pass

            # Send email and retrieve sent_status
            send_email_result = send_email(server, cred['smtp_user'], contact['contact_email_1'], parsed_dict['subject'], parsed_dict['content'])

            #Update the database if the email was sent successfully
            if send_email_result == True:
                contacts_collection.update_one(
                    {"_id": contact["_id"]},
                    {"$set": {"sent_status": True}},
                    upsert=True
                )
            elif send_email_result == 'limit_exceeded':
                # Remove the current credential from the cycle
                credential_list.remove(cred)
                credential_cycle = cycle(credential_list)

            server.quit()
        except smtplib.SMTPAuthenticationError as e: # 
            print(f"Authentication failed. Removing this credential from the sending email list.")
            # Remove the current credential from the cycle
            credential_list.remove(cred)
            credential_cycle = cycle(credential_list)
        except socket.error:
            print('Your PC may be offline. Exiting here...')
            break
        except Exception as e:
            print(f"Error occurred in sending email, {e}")
        
        time.sleep(time_interval)

if __name__ == "__main__":
    main()