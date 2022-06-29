from email.mime.text import MIMEText
import smtplib

from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

EMAIL_ADDRESS = 'ikp.pp.2022@gmail.com'
EMAIL_PASSWORD = 'pyozgrfamzcvlhdm'

logo_image = open("./static/images/hcp-banner.png")


file_to_open = Path("./static/email_templates/appointment_notification.html")

appointment_notification_file = open(file_to_open,"r", encoding='UTF8').read()
                    
               
def send_appointment_notification(emailData):
    msgRoot = MIMEMultipart('related')

    msgRoot['Subject'] = emailData['subject']
    msgRoot['From'] = emailData['from']
    msgRoot['To'] = emailData['to']

    msgRoot.preamble = '====================================================='

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    email_content = appointment_notification_file.format(
        emailData['date'],
        emailData['time'],
        emailData['type'],
        emailData['department'],
        emailData['room'],
        emailData['doctor']
    )

    msgText = MIMEText(email_content, 'html')
    msgAlternative.attach(msgText)

    banner_image = MIMEImage(open('./static/images/hcp-banner.png','rb').read())
    banner_image.add_header('Content-ID', '<image1>')

    msgRoot.attach(banner_image)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg=msgRoot)
        server.quit()
    except:
        print('Something went wrong')


# if __name__ == '__main__':    
#     emailDict = {
#         'subject':'Szpital HCP - powiadomienie',
#         'to': 'imufkbuimohdoqndkl@bvhrs.com',
#         'from':'Szpital HCP',
#         'date':'11-12-2037',
#         'time':'12:34',
#         'type':'xyz',
#         'department':'xyz',
#         'room':'213a',
#         'doctor':'Łuczak'
#     }
#     send_appointment_notification(emailDict)