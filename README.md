# Take-Home-SH

- Program to detect whether clinician is within bounds of zone and send alert within 5 minutes of individual leaving zone.

## Methods

- get_response(**id**) - returns geojson reponse of API Get request for clinician's location status based on id
- extract_shapes(**resp**) - takes in json creates and returns array of shapes: point for clinician location and polygons for expected zones
- check_location(**shapes**) - determines whether clinician lies within expected zone based on given array of shapes
- status_check(**id**) - abstracts get_response(), extract_shapes(), and check_location() into one method - checks status of clinician with the given id
- clin_iter() - iterates through each id (1-6) and checks the status of each clinician, sends email_alert() if clinician out of expected zone
- poll_status(**interval**, **total**) - calls clin_iter() every **interval** seconds until **total** min have passed
- email_alert(**id**) - sends email containing clinician ID to desired mailbox

## Libraries Used

- requests - for handling API GET requests to location API
- json - formatting, translating, and debugging json objects
- shapely - setup spatial analysis based on clinician location and expected zones
- time - to track time for API polling and record in status alerts
- smtplib, email - to send email alerts as needed from personal gmail (kingtjrules101@gmail.com)

