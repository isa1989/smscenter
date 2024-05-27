
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import xml.etree.ElementTree as ET
import requests
import json
import datetime
import hmac
import hashlib

from accounts.models import Account
from .models import SMS, MobisSettings
from .utils import calculate_signature, generate_control_id, get_task_id, generate_sms_xml, generate_delivery_xml,get_status_xml, has_xml_body, generate_bulk_sms_xml

 

def get_mobis_login_password():
    mobis_settings = MobisSettings.objects.first()
    if mobis_settings:
        return mobis_settings.login, mobis_settings.password
    else:
        # Handle the case where MobisSettings is not found
        return None, None



@csrf_exempt
@require_POST
def send_sms(request):
    try:
        data = json.loads(request.body)
        headers = request.META
        login, password = get_mobis_login_password()

        content_type = headers.get('CONTENT_TYPE')
        username = headers.get('HTTP_USER_NAME')
        signature = request.headers.get('Signature')
        
        if content_type.lower() != 'application/json':     
            return JsonResponse({"error": "Invalid content type"}, status=400)

        if not (username and signature):
            return JsonResponse({"error": "Missing username or signature"}, status=400)
            
        account = Account.objects.get(username=username)
        title = account.sms_provider_title.title
        api_key = account.apikey.filter(is_active=True).last()
        public_key = api_key.public_key
        private_key = api_key.private_key
        expected_signature = calculate_signature(data['oper_time'], public_key, private_key)

        if signature != expected_signature:
            return JsonResponse({"error": "Invalid signature"}, status=401)
        
        msisdn = data['msisdn']
        message = data['message']
        control_id = generate_control_id()
        is_bulk = data['is_bulk']
        if is_bulk:
            xml_str = generate_bulk_sms_xml(login, password, title, control_id, msisdn, str(message))
        else:
            xml_str = generate_sms_xml(login, password, title, control_id, msisdn, str(message))

        xml = ET.fromstring(xml_str)
        xml = ET.tostring(xml, encoding='utf8')
        headers = {'Content-Type': 'application/xml'}
        response = requests.post('https://sms.atatexnologiya.az/bulksms/api', data=xml, headers=headers)
        task_id=get_task_id(response)

        delivery_str = generate_delivery_xml(login, password, task_id)
        
        delivery_xml = ET.fromstring(delivery_str)
        delivery_xml = ET.tostring(delivery_xml, encoding='utf8')
        delivery_response = requests.post('https://sms.atatexnologiya.az/bulksms/api', data=delivery_xml, headers=headers)
        if has_xml_body(delivery_response.text):
            status=get_status_xml(delivery_response.text)
        else:
            
            status='0'

        
        sms = SMS.objects.create(
            control_id=control_id,
            account=account,
            api_key=api_key,
            msisdn=msisdn,
            status=status,
            task_id=task_id,
            is_bulk=is_bulk
        )   
        if response.status_code == 200:
            print("SMS sent successfully")
            return HttpResponse("SMS sent successfully", status=200)
        else:
            print("Failed to send SMS")
            return HttpResponse("Failed to send SMS", status=500)

    except Account.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)
    except KeyError as e:
        return JsonResponse({"error": f"Missing required field: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def update_sms_statuses():
    # Fetch all SMS objects with non-null task_id
    login, password = get_mobis_login_password()
    sms_to_update = SMS.objects.filter(task_id__isnull=False, status__in=[0,1])
    if sms_to_update:
        # Iterate over each SMS object and update its status  
        for sms in sms_to_update:
            # Generate XML for delivery request
            delivery_xml = generate_delivery_xml(login, password, sms.task_id)
            # Send request to get delivery status
            headers = {'Content-Type': 'application/xml'}
            response = requests.post('https://sms.atatexnologiya.az/bulksms/api', data=delivery_xml, headers=headers)
            # Check if response has XML body
            if has_xml_body(response.text):
                # Parse XML response
                root = ET.fromstring(response.text)
                for body in root.findall('.//body'):
                    status = body.find('status').text
                    # Update SMS object with msisdn and status
                    sms.status = status
                    sms.save()
            else:
                # Handle case where response does not have XML body
                return JsonResponse({"failed": "where response does not have XML body"})
    else:
        return JsonResponse({"error": "No SMS objects to update"})