from django.core.mail import EmailMessage
import os
import requests
from django.conf import settings
import random

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()

  def send_otp(mobile):
    try:
      otp = random.randint(1000,9999)
      # url = f'https://2factor.in/API/V1/{settings.OTP_API_KEY}/SMS/{mobile}/{otp}'
      # response = requests.get(url)
      # print(response)
      return otp

    except Exception as e:
      return None