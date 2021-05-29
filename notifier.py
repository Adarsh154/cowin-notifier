import smtplib
import time
from datetime import date
import requests
import sqlite3


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
                    if (session['min_age_limit'] == user[3]) and (session['available_capacity'] > 0):
                        names += str(centre['name']) + ","
            if names != '':
                send_mail(names[: -1], user[1])
        except Exception as e:
            send_mail(e, "aj1541998@gmail.com")
            continue


def send_mail(names, email):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("adarshtalesara2@gmail.com", "password")

    # message to be sent
    message = """Subject: Covid notification \n
    Vaccine Available at {}
    """.format(names)

    # sending the mail
    s.sendmail("adarshtalesara2@gmail.com", email, message)

    # terminating the session
    s.quit()


con = sqlite3.connect('users.sqlite3')
cursorObj = con.cursor()
while True:
    cursorObj.execute('SELECT * FROM user_data')
    rows = cursorObj.fetchall()
    current_date = date.today().strftime("%d-%m-%Y")
    check_avail(rows, current_date)