import io

from groq import Groq
from pprint import pprint

import smtplib, ssl
from email.mime.text import MIMEText

class sendSpam:
    
    def __init__(self, api_key, smtp_server, port, login, password, sender_email, reciver_email ):
        self.sender_email = sender_email
        self.reciver_email = reciver_email
        self.port = port
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.client = Groq(api_key=api_key)
    
    #--------- FUNCTIONS ------------

    def findEmail(self, mailText):
        """
        Finds text between strings "Hej BEST" and "Hilsen KBEST"
        ---
        Input: str
        Output: str
        """
        mailList = mailText.split()
       
        if "Hej" in mailList and any(i in mailList for i in ("BEST", "BEST,")):
            startIndex = mailList.index("Hej")
            while mailList[startIndex + 1][0:4] != "BEST":
                startIndex = mailList.index("Hej", startIndex)
        else:
            startIndex = 0
        
        if "Hilsen" and "KBEST" in mailList:
            endIndex = mailList.index("Hilsen")
            while mailList[endIndex + 1][0:5] != "KBEST":
                endIndex = mailList.index("Hilsen", endIndex)
        else:
            endIndex = len(mailList)


        newMail = " ".join(mailList[startIndex + 2:endIndex])

        return "Hej BEST. \n\n" + newMail + "\n\n Hilsen KBEST"


    def clean_list(self, toClean):
        """
        Cleans a list of "\\n" from the items list
        ----
        Paramenters
        --
        toClean : list
            It is a list of strings

        Returns
        --
        list 
            list of strings
        """
        newlist = []

        for x in toClean:
            if x != "\n":
                newlist.append(x.rstrip("\n"))
        return newlist


    def make_prompt(self, promptList):
        """
        Makes a list of prompts with a prompt prefix from a given list of prompts
        ----

        Paramenters
        --
        promptList : list
            It is a list of str

        Returns
        --
        list 
            a list of string with the prefix added
        """
        newList = self.clean_list(promptList)
        return ["Kan du skrive en mail på dansk, der starter med \"Hej BEST\" og slutter med \"Hilsen KBEST\" der spørger om " + x for x in newList]

    def send_email(self, subject, text):
        #Generate object
        message = MIMEText(text, "plain")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = self.reciver_email

        #Send email
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.login, self.password)
            server.sendmail(self.sender_email, self.reciver_email, message.as_string())

        print("sent")

    
    def send_email_with_ai(self, prompts, titles):

        try:
            promptsList = prompts.readlines()
            titleList = titles.readlines()
        except AttributeError:
            prompts_titles = prompts
            titleList = titles

        prompts_titles = tuple(zip(self.make_prompt(promptsList), self.clean_list(titleList)))


        for content in prompts_titles:
        
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": content[0], 
                    }
                ],
                model="llama3-8b-8192",
            )

            #Prints the email just to see what it is
            print(chat_completion.choices[0].message.content)
            print(self.findEmail(chat_completion.choices[0].message.content))

            #What to send
            text = self.findEmail(chat_completion.choices[0].message.content)

            self.send_email(content[1], text)


