
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import xml.etree.ElementTree as ET
import requests
import datetime

from accounts.models import Account
from .models import SMS, MobisSMSControlid, MobisSettings



@csrf_exempt
@require_POST
def send_sms(request):

    mobis = MobisSettings.get_solo()
    data = request.body
    headers = request.META
    try:
        content_type = headers.get('Content-Type')
        username = headers.get('User-Name')
        public_key = headers.get('Public-Key')
        private_key = headers.get('Private-Key')
        phone_number = data['phone']
        message = data['message']

        if content_type.lower() == 'application/json':
            account = Account.objects.get(username=username)
            title = account.sms_provider_title.name
            api_key = account.api_keys.get(public_key=public_key, private_key=private_key)
            control_id = MobisSMSControlid.objects.create(code=account.merchant_code)
            
            sms = SMS.objects.create(
                control_id=control_id,
                account=account,
                api_key=api_key,
                msisdn=phone_number
            )

            # MOBIS SMS

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
                '''.format(mobis.login, mobis.password, title, control_id, phone_number, str(message))
            
            xml = ET.fromstring(xml_str)
            xml = ET.tostring(xml, encoding='utf8')

            headers = {'Content-Type': 'application/xml'}
            requests.post('https://sms.atatexnologiya.az/bulksms/api', data=xml, headers=headers)
    
    except:
        pass
