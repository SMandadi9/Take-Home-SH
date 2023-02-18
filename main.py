import requests
import json
from shapely.geometry import shape, Point
import time

clin_json = {}

def get_response(id): # Returns dictionary containing information about location
    base_api = 'https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/'
    response = requests.get(base_api + str(id))
    clin_json[id] = json.dumps(response.json())
    return response.json()

def extract_shapes(resp): # Returns list containing [Clinician Point, Zone 1, Zone 2, ... , Final Zone], 
    pt_coord = resp['features'][0]['geometry']['coordinates']
    shapes = [Point(pt_coord)] 

    for s in resp['features'][1:]: # Iterates through zones if more than one zone
        poly = shape(s['geometry'])
        shapes.append(poly)

    return shapes

def check_location(shapes): # Checks whether phlebotomist is within given polygon shapes to a certain threshold
    pt = Point(shapes[0])

    for s in shapes[1:]:
        if s.distance(pt) < 1e-10: return True
    return False
    
def status_check(id): # abstracts get_response(), extract_shapes(), and check_location() methods
    resp = get_response(id)
    shapes = extract_shapes(resp)
    
    return check_location(shapes)


def clin_iter(): # checks status for each clinician in the system
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S %p", t)
    for id in range(1, 7):
        pres = status_check(id)
        if not pres:
            email_alert(id, current_time)


def poll_status(interval, total): # sends request to API every INTERVAL seconds until we reach TOTAL minute(s)
    curr_sec = 0
    total_sec = total * 60
    while curr_sec < total_sec:
        clin_iter()
        curr_sec += interval
        time.sleep(interval)

    print('Status Updates Complete')

import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
def email_alert(id, time_now): # sends an email regarding alert for ID at TIME
    msg = MIMEMultipart()
    msg['From'] = 'kingtjrules101@gmail.com'
    msg['To'] = 'coding-challenges+alerts@sprinterhealth.com'
    msg['Subject'] = 'URGENT ALERT: Sprinter Out of Zone!'
    message = 'Sprinter ' + str(id) + ' has exited the expected zone! Time of Report = ' + time_now + '\n\n' + 'Request Initiated by Suryateja Mandadi'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('kingtjrules101@gmail.com', 'qwoynyxmnyghzlfw')

    mailserver.sendmail('kingtjrules101@gmail.com','coding-challenges+alerts@sprinterhealth.com', msg.as_string())

    mailserver.quit()

def main():

    poll_status(60, 60) # polls every 60 seconds for 60 minutes


main()
