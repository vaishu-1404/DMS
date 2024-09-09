from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from api.models import *
from api.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
# for sending mails and generate token
from django.template.loader import render_to_string # used returns the resulting content as a string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode #  used to safely encode and decode data in a URL-friendly format
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError #  helps in managing string and byte conversions
from django.core.mail import EmailMessage # used to construct and send email messages
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render



# Client View's
class create_client(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_client(request):
    if request.method == 'GET':
        client = Client.objects.all()
        serializers = ClientSerializer(client, many=True)
        return Response(serializers.data)

@api_view(['PUT'])
def edit_client(request,pk):
    if request.method == 'PUT':
        client = Client.objects.get(id=pk)
        client_serializer = ClientSerializer(instance=client, data=request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response('Client Updated')
        return Response(client_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_client(request,pk):
    if request.method == 'DELETE':
        client = Client.objects.get(id=pk)
        client.delete()
        return Response ('Company Deleted')
    return Response ('Fail to delete')

@api_view(['GET'])
def detail_client(request,pk):
    client = Client.objects.get(id=pk)
    view_bank = Bank.objects.filter(client=client)
    view_owner = Owner.objects.filter(client=client)
    view_dashboarduser = CustomUser.objects.filter(client=client)
    view_clientuser = CustomUser.objects.filter(client=client)

    client_serializer = ClientSerializer(client)
    bank_serializer = BankSerializer(view_bank, many=True)
    owner_serializer = OwnerSerializer(view_owner, many=True)
    view_dashboarduser = UserSerializerWithToken(view_dashboarduser, many=True)
    view_clientuser = UserSerializerWithToken(view_clientuser, many=True)

    data ={
        'client' : client_serializer.data,
        'bank' : bank_serializer.data,
        'owner' : owner_serializer.data,
        'dashboarduser' : view_dashboarduser.data,
        'clientuser' : view_clientuser.data
    }
    return Response(data)

# Bank View's

@api_view(['POST'])
def create_bank(request, pk):
    client = get_object_or_404(Client, id=pk)
    if request.method == 'POST':
        # client = Client.objects.get(id=client_pk)
        bank_serializer = BankSerializer(data=request.data)
        if bank_serializer.is_valid():
            bank_serializer.save(client=client)
            return Response(bank_serializer.data, status=status.HTTP_201_CREATED)
        return Response(bank_serializer.error,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_bank(request,pk,bank_pk):
    client = get_object_or_404(Client, id=pk)
    bank = Bank.objects.get(id = bank_pk)
    if request.method == 'PUT':
        bank_serializer = BankSerializer(data=request.data, instance=bank)
        if bank_serializer.is_valid():
            bank_serializer.save(client=client)
            return Response('Bank Updated')
        return Response(bank_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_bank(request, pk):
    client = Client.objects.get(id=pk)
    bank_list = Bank.objects.filter(client=client)
    serializers = BankSerializer(bank_list,many=True)
    print(serializers)
    return Response(serializers.data)

@api_view(['DELETE'])
def delete_bank(request,pk, bank_pk):
    client = get_object_or_404(Client, id=pk)
    bank = Bank.objects.get(id=bank_pk)
    if request.method == 'DELETE':
        bank.delete()
        return Response('Bank is Deleted')
    return Response('Fail to Delete Bank')

# Owners View's

@api_view(['POST'])
def create_owner(request, pk):
    client = get_object_or_404(Client, id=pk)
    if request.method == 'POST':
        owner_serializer = OwnerSerializer(data=request.data)
        if owner_serializer.is_valid():
            owner_serializer.save(client=client)
            return Response(owner_serializer.data,status=status.HTTP_201_CREATED)
        return Response(owner_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_owner(request, pk, owner_pk):
    client = get_object_or_404(Client, id= pk)
    owner = Owner.objects.get(id = owner_pk)
    if request.method == 'PUT':
        owner_serializer = OwnerSerializer(data=request.data, instance=owner)
        if owner_serializer.is_valid():
            owner_serializer.save(client=client)
            return Response('Owner Updated')
        return Response(owner_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_owner(request, pk):
    client = Client.objects.get(id = pk)
    owner_list = Owner.objects.filter(client=client)
    serializers = OwnerSerializer(owner_list, many=True)
    print(serializers)
    return Response(serializers.data)


@api_view(['DELETE'])
def delete_owner(request, pk, owner_pk):
    client = get_object_or_404(Client, id=pk)
    owner = Owner.objects.get(id = owner_pk)
    if request.method == 'DELETE':
        owner.delete()
        return Response('Owner is deleted')
    return Response('Failed to delete owner')


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['email'] = user.email
#         # ...

#         return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
             data[k]=v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated]) # the user should be valid
def getUserProfile(request):
    user = request.user # to get the specific user
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser]) # the user should be an admin only
def getUsers(request):
    user = CustomUser.objects.all() # to get the list of all users
    serializer = UserSerializerWithToken(user, many=True)
    return Response(serializer.data)

# Dashboard User Form
@api_view(['POST'])
def dashboarduser(request):
    # client = get_object_or_404(Client, id=pk)
    data = request.data
    try:
        user = CustomUser.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['email'],
                                     email=data['email'],password=make_password(data['password']), is_active=False)
        # generate token for email sending
        email_subject = "Activate You Account"
        message = render_to_string(
            "activate.html",
            {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user),
            }
        )
        # print(message)
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[data['email']])
        email_message.send()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'User Already Exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# Client User Form
@api_view(['POST'])
def clientuser(request,pk):
    client = get_object_or_404(Client, id=pk)
    data = request.data
    try:
        user = CustomUser.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['email'],
                                     email=data['email'],password=make_password(data['password']), is_active=False)
        # generate token for email sending
        email_subject = "Activate You Account"
        message = render_to_string(
            "activate.html",
            {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : generate_token.make_token(user),
            }
        )
        # print(message)
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[data['email']])
        email_message.send()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'User Already Exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid= force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,"activatesuccess.html")
        else:
            return render(request,"activatefail.html")


