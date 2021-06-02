import logging
import smtplib
import time
from datetime import date
from config import Email_app_password,db_password
import mysql.connector
import requests

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database="users"
)
logging.basicConfig(filename="std.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Let us Create an object
logger = logging.getLogger()

# Now we are going to Set the threshold of logger to Info
logger.setLevel(logging.INFO)


# try:
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#
#     # start TLS for security
#     s.starttls()
#
#     # Authentication
#     s.login("adarshtalesara2@gmail.com", "password")
#     s.quit()
# except Exception as e:
#     logger.info(e)


def check_avail(users, current_date):
    for user in users:
        time.sleep(3)
        try:

            names = ''
            header = {
                'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/90.0.4430.212 Safari/537.36'}
            x = requests.get(
                url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?',
                headers=header, params={"district_id": user[2][:3], "date": current_date})
            locations = x.json()
            for centre in locations['centers']:
                for session in centre['sessions']:
                    if (session['min_age_limit'] == user[3]) and (session[user[4]] > 0):
                        if centre['name'] not in names:
                            names += str(centre['name']) + ","
            if names != '':
                logger.info("Triggered")
                send_mail(names[: -1], user[1])
        except Exception as email_send:
            logger.error(email_send)
            continue


def send_mail(names, email):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("adarshtalesara2@gmail.com", Email_app_password)
    # message to be sent
    message = """Subject: Covid notification \n
    Vaccine Available at {}
    """.format(names)

    # sending the mail
    s.sendmail("adarshtalesara2@gmail.com", email, message)

    # terminating the session
    s.quit()
    mycursor2 = mydb.cursor()
    mycursor2.execute("Delete FROM user_data WHERE email='{}'".format(email))
    mydb.commit()


while True:
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM user_data")

    rows = mycursor.fetchall()
    current_date = date.today().strftime("%d-%m-%Y")
    check_avail(rows, current_date)
