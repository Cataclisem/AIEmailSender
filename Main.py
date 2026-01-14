from groq import Groq
from pprint import pprint
from email.mime.text import MIMEText
from sendSpam import sendSpam
import os
from dotenv import load_dotenv
load_dotenv()



#Server setup
port = os.getenv("port")
smtpServer = os.getenv("smtpServer")

#Login
login = os.getenv("emailLogin")
password = os.getenv("emailPassword")

#Emails
sender_email = os.getenv("sender_email")
reciver_email = os.getenv("reciver_email")
#Prompts
prompts = open("emailPrompts.txt", "r", encoding="utf-8")

titles = open("emailTitles.txt", "r", encoding="utf-8")


#Api key, plz dont share
GPT_api_key = os.getenv("apiKey")
client = Groq(api_key=GPT_api_key)

#--------- CODE ----------

ss_real = sendSpam(GPT_api_key, smtpServer, port, login, password, sender_email, reciver_email)

ss_fake = sendSpam(GPT_api_key, "localhost", 1025, "", "", sender_email, reciver_email)

ss_real.send_email_with_ai(prompts, titles)
