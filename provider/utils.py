
import hashlib
from random import randint
import xml.etree.ElementTree as ET
from .models import SMS


def calculate_signature(time, public_key, private_key):
    data = time + public_key + private_key
    encoded_data = data.encode('utf-8')
    
    # Calculate SHA-256 hash of the encoded data
    sha256_hash = hashlib.sha256(encoded_data)
    return sha256_hash.hexdigest()
 

def generate_control_id():
    control_id = str(randint(10000000000000000000, 100000000000000000000))
    while SMS.objects.filter(control_id=control_id).exists():
            control_id = str(randint(10000000000000000000, 100000000000000000000))
    return control_id



def get_task_id(response):
    # Get the content of the response
    xml_response = response.content.decode('utf-8')  # Decode bytes to UTF-8 string
    # Parse the XML
    root = ET.fromstring(xml_response)
    # Find the taskid element
    taskid_element = root.find('.//taskid')
    # Extract and return the taskid value
    if taskid_element is not None:
        taskid = taskid_element.text
        return taskid
    else:
        return None  # Or raise an exception if you prefer



def generate_sms_xml(login, password, title, control_id, msisdn, message):
    xml_str = '''<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <head>
                <operation>submit</operation>
                <login>{}</login>
                <password>{}</password>
                <title>{}</title>
                <scheduled>now</scheduled>
                <isbulk>false</isbulk>
                <controlid>{}</controlid>
            </head>
            <body>
                <msisdn>{}</msisdn>
                <message>{}</message>
            </body>
        </request>
        '''.format(login, password, title, control_id, msisdn, message)
    return xml_str


def generate_bulk_sms_xml(login, password, title, control_id, msisdn, message):
    body=""
    for ms in msisdn:
        body += f"<body>\n<msisdn>{ms}</msisdn>\n</body>\n"
    xml_str = '''<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <head>
                <operation>submit</operation>
                <login>{}</login>
                <password>{}</password>
                <title>{}</title>
                <bulkmessage>{}</bulkmessage>
                <scheduled>now</scheduled>
                <isbulk>true</isbulk>
                <controlid>{}</controlid>
            </head>
            {}
        </request>
        '''.format(login, password, title, message, control_id, body)
    return xml_str


def generate_delivery_xml(login, password, task_id):
    delivery_str = '''<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <head>
                <operation>detailedreport</operation>
                <login>{}</login>
                <password>{}</password>
                <taskid>{}</taskid>
            </head>
        </request>
        '''.format(login, password, task_id)
    return delivery_str


def get_status_xml(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Find the 'status' element within the 'body'
    body = root.find('body')
    if body is not None:
        status_element = body.find('status')
        if status_element is not None:
            status = status_element.text
            # If status is 4 or 5, save it as 3
            if status in ['4', '5']:
                return '3'
            return status

    # Return None if 'status' element is not found
    return None


def has_xml_body(xml_string):
    root = ET.fromstring(xml_string)
    response_code = root.find('head/responsecode').text
    body_element = root.find('body')
    if body_element is not None:
        return True
    return False


# def update_last_statuses():
#     smss=SMS.objects.filter(status__in=[1,2])