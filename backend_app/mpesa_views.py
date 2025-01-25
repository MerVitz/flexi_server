import requests
import base64
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json().get("access_token")

@csrf_exempt
def stk_push_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            access_token = get_mpesa_access_token()

            # Log the access token for debugging purposes
            print(f"Access Token: {access_token}")

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

            # Log the password for debugging purposes
            print(f"Password: {password}")

            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": data["amount"],
                "PartyA": data["phone"],  
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": data["phone"],
                "CallBackURL": settings.CALLBACK_URL,
                "AccountReference": "Order123",
                "TransactionDesc": "Payment for Order123"
            }

            # Log payload for debugging purposes
            print(f"Payload: {json.dumps(payload, indent=4)}")

            response = requests.post(
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers,
            )

            return JsonResponse(response.json())

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def mpesa_webhook(request):
    try:
        data = json.loads(request.body)
        print("M-Pesa Payment Received:", data)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Error processing request"})

