import os
from venv import create
from dotenv import load_dotenv
import tweepy
import requests
import logging
import random
import time
import threading

logging.basicConfig(level=logging.INFO)

# Load environmental variables
load_dotenv("e_variables.env")

FILE_NAME = "last_seen_id.txt"
USER_ID = os.environ.get("USER_ID")
SLEEPING_TIME = 15

def retrieve_last_seen_id(file_name):
    with open(file_name, "r") as f:
        last_seen_id = int(f.read().strip())
    return last_seen_id

def store_last_seen_id(file_name, last_seen_id):
    with open(file_name, "w") as f:
        f.write(str(last_seen_id))

common_drugs = ["paracetamol", "aspirin", "ibuprofen", "atorvastatin", "alcohol", "amoxicillin", "lisinopril", "omeprazole", "losartan", "metoprolol", "levothyroxine", "metformin", "amlodipine", "albuterol", "simvastatin", "cocaine", "cannabis", "sertraline", "furosemide", "tramadol", "clonazepam", "oxycodone", "venlafaxine", "fluticasone", "pantoprazole"]

client = tweepy.Client(
        bearer_token= os.environ.get("bearer_token"),
        consumer_key= os.environ.get("consumer_key"),
        consumer_secret= os.environ.get("consumer_secret"),
        access_token= os.environ.get("access_token"),
        access_token_secret= os.environ.get("access_token_secret")
        )

class Drugs:

    def __init__(self):
        self.drug_name_1 = ""
        self.drug_name_2 = ""
        self.rxcui_1 = ""
        self.rxcui_2 = ""
        self.warning = True
        self.description = "Sorry, the format is not correct."

    def get_warning(self):
        return self.warning

    def get_description(self):
        return self.description

    def get_rxcui_1(self):
        return self.rxcui_1
    
    def get_rxcui_2(self):
        return self.rxcui_2

    def get_drug_name_1(self):
        return self.drug_name_1

    def get_drug_name_2(self):
        return self.drug_name_2

    # Get names from mentioned tweet
    def tweet_to_data(self, tweet_text):
        try:
            # Check tweet format
            text = tweet_text.split(" ")
        except:
            logging.info("The user input could not be .split()")
            self.warning = False
            self.description = "Sorry, there was a problem processing your tweet."
            # client.create_tweet(text="Sorry, there was a problem processing your tweet.", in_reply_to_tweet_id=tweet_id)
        else:
            if len(text) == 3 or len(text) == 4:
                self.drug_name_1 = text[1]
                self.drug_name_2 = text[2]
            else:
                #Check if there are more than two inputs in the tweet
                self.warning = False
                self.description = "Sorry, the format is not correct."
                logging.info("There are more than 3 inputs")
                # client.create_tweet(text="Sorry, the format is not correct.", in_reply_to_tweet_id=tweet_id)

    # Automated tweet
    def sample_tweet(self, common_drugs_list):
        drugs_sample = random.sample(common_drugs_list, 2)
        self.drug_name_1 = drugs_sample[0]
        self.drug_name_2 = drugs_sample[1]

    # Retrieve the drugs ids and populate the dict
    def get_drug_rxcui(self):
        # Get ID for drug1
        r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={self.drug_name_1}&search=2')
        if r.status_code == 200:
            answer = r.json()
            try:
                rxcui = answer['idGroup']['rxnormId'][0]
            except:
                self.rxcui_1 = "not found"
            else:
                self.rxcui_1 = rxcui
        else:
            self.warning = False
            self.description = "Sorry, there was a problem processing your tweet."
            logging.error(r.url)
            logging.error(r.status_code)

        
        # Get ID for drug2
        r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={self.drug_name_2}&search=2')
        if r.status_code == 200:
            answer = r.json()
            try:
                rxcui = answer['idGroup']['rxnormId'][0]
            except:
                self.rxcui_2 = "not found"
            else:
                self.rxcui_2 = rxcui 
        else:
            self.warning = False
            self.description = "Sorry, there was a problem processing your tweet."
            logging.error(r.url)
            logging.error(r.status_code)   
        

    # Check the drug id was found for both drugs
    def check_rxcuis(self):
        answer = []
        if self.rxcui_1 == "not found":
            answer.append(f'Sorry, the drug {self.drug_name_1} you are looking for was not found.')
            self.warning = False
        if self.rxcui_2 == "not found":
            answer.append(f'Sorry, the drug {self.drug_name_2} you are looking for was not found.')
            self.warning = False
        else:
            logging.info("Both drugs found")
        if self.rxcui_1 == "not found" or self.rxcui_2 == "not found":
            self.description = " ".join(answer)

    # Retrieve the possible interaction between drugs
    def get_interactions(self):
        # format for request: drug1+drug2
        r = requests.get(f'https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={self.rxcui_1}+{self.rxcui_2}')
        if r.status_code == 200:
            answer = r.json()
            try:
                interaction = answer['fullInteractionTypeGroup'][0]['fullInteractionType'][0]['interactionPair'][0]['description']
            except:
                self.warning = False
                self.description = "I could not find any interactions between those drugs."
                logging.info("no description found")
            else:
                self.warning = True
                self.description = interaction
        else:
            self.warning = False
            logging.error(r.url)
            logging.error(r.status_code)


# Reply tweets mentions
def reply_mentioned_tweets():
    while True:
        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        tweets = client.get_users_mentions(id=USER_ID, since_id=last_seen_id)
        try:
            # Check if there are any new tweets by trying to reverse the data 
            reversed(tweets.data)
        except:
            logging.info("No new tweets")
        else:
            for tweet in reversed(tweets.data):
                logging.info("Checking tweet of id: " + str(tweet.id))
                # Like tweet
                client.like(tweet_id=tweet.id)

                # Drugs processing
                drugs = Drugs()

                # Get RXCUI IDs for drugs 
                drugs.tweet_to_data(tweet.text)
                if drugs.warning == False:
                    client.create_tweet(text=drugs.description, in_reply_to_tweet_id=tweet.id)
                    last_seen_id = tweet.id
                    store_last_seen_id(FILE_NAME, last_seen_id)
                    continue

                drugs.get_drug_rxcui()
                if drugs.warning == False:
                    client.create_tweet(text=drugs.description, in_reply_to_tweet_id=tweet.id)
                    last_seen_id = tweet.id
                    store_last_seen_id(FILE_NAME, last_seen_id)
                    continue

                # Check if there was possible to retrieve any drug ID
                drugs.check_rxcuis()
                if drugs.warning == False:
                    client.create_tweet(text=drugs.description, in_reply_to_tweet_id=tweet.id)
                    last_seen_id = tweet.id
                    store_last_seen_id(FILE_NAME, last_seen_id)
                    continue

                drugs.get_interactions()
                client.create_tweet(text=drugs.description, in_reply_to_tweet_id=tweet.id)

                # Store the last tweet processed
                last_seen_id = tweet.id
                store_last_seen_id(FILE_NAME, last_seen_id)
        finally:
            logging.info("Sleeping for {} seconds".format(SLEEPING_TIME))
            time.sleep(SLEEPING_TIME)


def random_tweets():
    while True:
        drugs = Drugs()
        drugs.sample_tweet(common_drugs)
        logging.info(f'Trying {drugs.drug_name_1} and {drugs.drug_name_2}')
        drugs.get_drug_rxcui()

        drugs.check_rxcuis()
        if drugs.warning == False:
            continue
    
        drugs.get_interactions()
        if drugs.warning == False:
            continue

        new_tweet = [f'#{drugs.drug_name_1} & #{drugs.drug_name_2}', drugs.description]
        client.create_tweet(text="\n".join(new_tweet))
        time.sleep(3600)

t1 = threading.Thread(target=reply_mentioned_tweets)  
t2 = threading.Thread(target=random_tweets)

def main():
    t1.start()
    t2.start()

if __name__ == "__main__":    
    main()
    