import getpass
import poplib
import email
import os
import smtplib
import email.utils
from email.mime.text import MIMEText
print("Welcome to this minimal POP3/SMTP Mail Client")

user = input("Username: ")
password = input("Password: ")


def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)


def readMail(user, password):
    Mailbox = poplib.POP3_SSL('pop-mail.outlook.com', '995')
    password = (password)
    Mailbox.user(user)
    Mailbox.pass_(password)
    numMessages = len(Mailbox.list()[1])
    for i in range(numMessages-5, numMessages):
        raw_email = b"\n".join(Mailbox.retr(i+1)[1])
        parsed_email = email.message_from_bytes(raw_email)
        print('=========== email #%i ============' % i)
        print('From:', parsed_email['From'])
        print('To:', parsed_email['To'])
        print('Date:', parsed_email['Date'])
        print('Subject:', decode_header(parsed_email['Subject']))
        print('=========== email #%i ended ============' % i)

    back = input("Type back to go back to the menu: ")
    while(back.lower() != "back"):
        back = input("Type back to go back to the menu: ")
    menu()


def sendMail(user, password):
    TO = input("To who: ")
    SUBJECT = input("What's the subject: ")
    TEXT = input("What's the message: ")
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)

    BODY = '\r\n'.join(['To: %s' % TO, 'From: %s' % user,
                       'Subject: %s' % SUBJECT, '', TEXT])
    server.sendmail(user, [TO], BODY)
    print ('email sent')
    server.quit()
    back = input("Type back to go back to the menu: ")
    while(back.lower() != "back"):
        back = input("Type back to go back to the menu: ")
    menu()


def menu():
    print("1. Read mail")
    print("2. Send mail")
    print("3. Exit")

    chosenOption = input("Give the number of the option you want to do: ")
    if(chosenOption == "1"):
        readMail(user, password)
    elif(chosenOption == "2"):
        sendMail(user, password)
    else:
        os._exit
menu()
