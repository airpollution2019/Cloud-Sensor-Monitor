import smtplib

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

CO2 = 0
SO2 = 0
NO2 = 0

R_NO2_Level = 100
R_SO2_Level = 100
R_CO2_Level = 100

WARN_CO2_Level = 200
WARN_SO2_Level = 200
WARN_NO2_Level = 200

TO_ADDRS = ['shubhamdd.97@gmail.com','keith.quadros12@gmail.com','1996rohitsaigal@gmail.com']

SENDER_MAIL_SERVER = 'smtp.mail.yahoo.com'
SENDER_MAIL_PORT = 587
SENDER_MAIL_ID = "temp_bot_mailer@yahoo.com"
SENDER_MAIL_PASS = 'mailerbottemp'


@app.route('/')
def index():
    return render_template('index.html',
                           R_NO2_Level=R_NO2_Level,
                           R_CO2_Level=R_CO2_Level,
                           R_SO2_Level=R_SO2_Level)


@app.route('/data')
def data():
    co2 = request.args.get('CO2')
    so2 = request.args.get('SO2')
    no2 = request.args.get('NO2')

    global CO2
    global SO2
    global NO2

    CO2 = int(co2)
    SO2 = int(so2)
    NO2 = int(no2)

    print("CO2:{} SO2:{} NO2:{}".format(CO2, SO2, NO2))

    if not check_levels_below_threshold(co2=int(co2), no2=int(no2), so2=int(so2)):
        print("Warning! Levels above the threshold.")
        message = "Warning!\n " \
                  "Air Quality Critical!\n " \
                  "CO2:{co2}\n" \
                  "SO2:{so2}\n" \
                  "NO2:{no2}".format(co2=co2, no2=no2, so2=so2)
        send_mail(to_addrs=TO_ADDRS, message=message)

    return "CO2:{} SO2:{} NO2:{}".format(CO2, SO2, NO2)


@app.route('/get-data')
def get_data():
    resp = {"CO2": CO2,
            "SO2": SO2,
            "NO2": NO2}

    return jsonify(resp)


def check_levels_below_threshold(co2, no2, so2):
    if co2 <= WARN_CO2_Level:
        if no2 <= WARN_NO2_Level:
            if so2 <= WARN_SO2_Level:
                return True
    return False


def send_mail(to_addrs, message):
    print("Sending Mail, To:{} Message:{}".format(to_addrs, message))

    try:
        server = smtplib.SMTP(SENDER_MAIL_SERVER, SENDER_MAIL_PORT)
        server.set_debuglevel(True)
        server.starttls()
        server.login(SENDER_MAIL_ID, SENDER_MAIL_PASS)
        server.sendmail(from_addr=SENDER_MAIL_ID, to_addrs=to_addrs, msg=message)
        server.quit()
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        print("Error: unable to send email", str(e))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)
