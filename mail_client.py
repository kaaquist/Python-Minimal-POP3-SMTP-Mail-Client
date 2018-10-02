import getpass
import poplib
import email
import os
import smtplib

"""Hacktoberfest 2""""

print("Welcome to this minimal POP3/SMTP Mail Client")
print("What email provider do you use?")
print("1. outlook")
print("2. yahoo")

POP_PORT = 995
SMTP_PORT = 587

chosen_option = input("Give the number of the provider you use: ")
if(chosen_option == "1"):
    pop_server = "pop-mail.outlook.com"
    smtp_server = "smtp-mail.outlook.com"
else:
    pop_server = "pop.mail.yahoo.com"
    smtp_server = "smtp.mail.yahoo.com"

user = input("Username: ")
password = input("Password: ")


def decode_header(header):
    decoded_bytes, charset = email.header.decode_header(header)[0]
    if charset is None:
        return str(decoded_bytes)
    else:
        return decoded_bytes.decode(charset)


def read_mail(user, password, pop_server, smtp_server, SMTP_PORT, POP_PORT):
    mailbox = poplib.POP3_SSL('pop-mail.outlook.com', '995')
    password = (password)
    mailbox.user(user)
    mailbox.pass_(password)
    num_messages = len(mailbox.list()[1])
    for i in range(num_messages-5, num_messages):
        raw_email = b"\n".join(mailbox.retr(i+1)[1])
        parsed_email = email.message_from_bytes(raw_email)
        print('=========== email #%i ============' % i)
        print('From:', parsed_email['From'])
        print('to:', parsed_email['to'])
        print('Date:', parsed_email['Date'])
        print('Subject:', decode_header(parsed_email['Subject']))
        print('=========== email #%i ended ============' % i)
    input("Press enter to go back to menu")
    menu()


def send_mail(user, password, pop_server, smtp_server, SMTP_PORT, POP_PORT):
    to = input("To who: ")
    subject = input("What's the subject: ")
    text = input("What's the message: ")
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)

    body = '\r\n'.join(['To: %s' % to, 'From: %s' % user,
                       'Subject: %s' % subject, '', text])
    server.sendmail(user, [to], body)
    print ('email sent')
    server.quit()
    input("Press enter to go back to menu")
    menu()


def menu():
    print("1. Read mail")
    print("2. Send mail")
    print("3. Exit")

    chosen_option = input("Give the number of the option you want to do: ")
    if(chosen_option == "1"):
        read_mail(user, password, pop_server, POP_PORT, smtp_server, SMTP_PORT)
    elif(chosen_option == "2"):
        send_mail(user, password, pop_server, POP_PORT, smtp_server, SMTP_PORT)
    else:
        os._exit
menu()
