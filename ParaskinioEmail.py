import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MY_ADDRESS = input('Enter your gmail adress: ')
PASSWORD = input('Enter your password: ')
Subject = input('Enter email subject: ')

filename = 'C:/Users/Odysseas/Desktop/ΠΑΡΑΣΚΗΝΙΟ/ΑΠΟΣΤΟΛΗ EMAIL/contacts.txt'
def get_contacts(filename):

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

filename = 'C:/Users/Odysseas/Desktop/ΠΑΡΑΣΚΗΝΙΟ/ΑΠΟΣΤΟΛΗ EMAIL/message.txt'
def read_template(filename):


    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    names, emails = get_contacts('C:/Users/Odysseas/Desktop/ΠΑΡΑΣΚΗΝΙΟ/ΑΠΟΣΤΟΛΗ EMAIL/offices.txt')
    message_template = read_template('C:/Users/Odysseas/Desktop/ΠΑΡΑΣΚΗΝΙΟ/ΑΠΟΣΤΟΛΗ EMAIL/message.txt')


    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.connect('smtp.gmail.com', 587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)


    for name, email in zip(names, emails):
        msg = MIMEMultipart()

        message = message_template.safe_substitute(OFFICE_NAME=name.title())
        print('To: ' + name.title() + ' \n')
        print(message)

        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = Subject

        msg.attach(MIMEText(message, 'plain'))
        pdfname = input('Directory of PDF file you will send: ')
        if(pdfname != ''):
            binary_pdf = open(pdfname, 'rb')
            payload = MIMEBase('application', 'octate-stream', Name=pdfname)
            payload.set_payload((binary_pdf).read())
            encoders.encode_base64(payload)
            payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
            msg.attach(payload)
        s.send_message(msg)
        if(pdfname != ''):
            print('ATTACHMENT SENT')
        del msg

    s.quit()

if __name__ == '__main__':
    main()
