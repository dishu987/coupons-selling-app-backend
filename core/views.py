from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from core.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,CouponSerializer
from django.contrib.auth import authenticate
from core.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from core.models import CouponModel,UserModel,OTPModel
from django.forms.models import model_to_dict
from core.utils import Util
import datetime


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class SendOTPView(APIView):
  def post(self,request,format=None):
      mobile = request.data['mobile']
      if mobile is None:
        return Response({
            'status':400,
            'message':"Mobile field is required"
          })

      if len(mobile) !=10:
        return Response({
            'status':400,
            'message':"Please give a valid mobile number"
          })
      if_exist = OTPModel.objects.filter(mobile=mobile)
      if if_exist:
        return Response({
            'status':400,
            'message':"Account on this number already exist"
          })
      otp = Util.send_otp(mobile)
      print(otp)
      new_mobile = OTPModel.objects.create(
        mobile=mobile,
        otp=otp
      )
      new_mobile.save()
      return Response({
        'status':200,
        'message':'Otp sent successfuly'
      })

class VerifyOTPView(APIView):
    def post(self,request,format=None):
      otp = request.data['otp']
      mobile = request.data['mobile']
      if mobile is None:
        return Response({
            'status':400,
            'message':"Mobile field is required"
          })
      if otp is None:
        return Response({
            'status':400,
            'message':"Otp field is required"
          })
      try:
        mobile_obj = OTPModel.objects.get(mobile=mobile)
      except Exception as e:
        return Response({
          'status':400,
          'message':'Mobile number is not valid'
        })
      if mobile_obj.is_verified:
        return Response({
            'status':400,
            'message':'Yours mobile number is already verified.'
          })
      if mobile_obj.otp==otp:
          mobile_obj.is_verified = True
          mobile_obj.save()
          return Response({
            'status':200,
            'message':'Mobile Varified'
          })
      
      return Response({'status':400,'message':'Invalid OTP'})


class ResendOTPView(APIView):
  def post(self,request,format=None):
    mobile = request.data['mobile']
    if mobile is None:
      return Response({
            'status':400,
            'message':"Mobile field is required"
          })
    if len(mobile) < 10:
        return Response({
            'status':400,
            'message':"Please give a valid mobile number"
          })
    try:
      get_mobile = OTPModel.objects.get(mobile=mobile)
    except Exception as e:
        return Response({
          'status':400,
          'message':'Mobile number is not valid'
        })
    otp = Util.send_otp(mobile)
    get_mobile.otp = otp
    get_mobile.is_verified=False
    get_mobile.save()
    return Response({
        'status':200,
        'message':'Otp sent successfuly'
      })

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)



class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
class UserProfileShowView(APIView):
  renderer_classes = [UserRenderer]
  def get(self, request, format=None):
    userid = self.request.query_params.get('userid')
    try:
      user = UserModel.objects.get(id=userid)
      data = {
      "email":user.email,
      "name":user.name,
      "mobile":user.mobile,
      "hostel":user.hostel,
      "room":user.room,
      "degree":user.degree,
      "batch":user.batch,
      }
      return Response(data, status=status.HTTP_200_OK)
    except:
      return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class CouponsListView(APIView):
  renderer_classes = [UserRenderer]
  def get(self, request, format=None):
    coupons = CouponModel.objects.all().order_by("-id")
    for coupon in coupons:
      if coupon.date<datetime.date.today():
        coupon.expired = True
        coupon.save()
    serializer = CouponSerializer(coupons,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CouponsCreateView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    data = {
      "user":request.user.id,
      "title":request.data["title"],
      "price":request.data["price"],
      "mess":request.data["mess"],
      "date":request.data["date"],
      "time":request.data["time"]
    }
    serializer = CouponSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    coupon = serializer.save()
    return Response({'msg':'Coupon Added Successful'}, status=status.HTTP_201_CREATED)

class CouponsDeleteView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    try:
      id = request.data["id"]
      coupon_instance = CouponModel.objects.filter(id=id,user = request.user)
      if not coupon_instance:
        return Response({'msg':'Invalid Id'},status=status.HTTP_400_BAD_REQUEST)
      coupon_instance.delete()
      return Response({'msg':'Coupon Deleted Successfully'}, status=status.HTTP_200_OK)
    except:
      return Response({'msg':'Id required'},status=status.HTTP_400_BAD_REQUEST)



