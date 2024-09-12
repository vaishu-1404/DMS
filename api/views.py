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
# from django.views.decorators.csrf import csrf_exempt


#  *******************************************Client View's***********************************************
class create_client(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Client Created'}, status=status.HTTP_201_CREATED)
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

# ***********************************************Bank View's******************************************************

@api_view(['POST'])
def create_bank(request, pk):
    client = get_object_or_404(Client, id=pk)
    if request.method == 'POST':
        # client = Client.objects.get(id=client_pk)
        bank_serializer = BankSerializer(data=request.data)
        if bank_serializer.is_valid():
            bank_serializer.save(client=client)
            return Response({'Message':'Bank Created'}, status=status.HTTP_201_CREATED)
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

# **********************************************Owners View's*******************************************

@api_view(['POST'])
def create_owner(request, pk):
    client = get_object_or_404(Client, id=pk)
    if request.method == 'POST':
        owner_serializer = OwnerSerializer(data=request.data)
        if owner_serializer.is_valid():
            # sum of a for loop values of share of all the owners created
            total_shares = sum([owner.share for owner in Owner.objects.all()])
            # calculating remaining shares by subtracting total shares by 100
            remaining_shares = 100 - total_shares
            # new share means the value of share while creating this owner
            new_share = owner_serializer.validated_data['share']

            if new_share > remaining_shares:
                # if enterd shares are greater then remaining share send a message of remaining shares
                return Response ({
                    'error': f'Cannot assign {new_share}%. Only {remaining_shares}% is left for assigning'
                }, status=status.HTTP_400_BAD_REQUEST)
            # save the all the data
            owner_serializer.save(client=client)
            return Response({'Message':'Owner Created'}, status=status.HTTP_201_CREATED)
        # show error if given data is not valid
        return Response(owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def edit_owner(request, pk, owner_pk):
    client = get_object_or_404(Client, id= pk)
    owner = Owner.objects.get(id = owner_pk)
    if request.method == 'POST':
        owner_serializer = OwnerSerializer(data=request.data, instance=owner)
        if owner_serializer.is_valid():
            owner_serializer.save(client=client)
            return Response('Owner Updated')
        return Response(owner_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        owner_serializer1 =OwnerSerializer(owner)
        return Response(owner_serializer1.data)

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
    try :
        # storing the value of current owner shares in a variable
        owner_share = owner.share
        owner.delete()
        # for loop for providing the remainig shares left
        total_shares = sum([owner.share for owner in Owner.objects.all()])
        remaining_shares = 100 - total_shares
        return Response({'message': f'Owner is deleted.{owner_share}% share is added back. Avaliable shares: {remaining_shares}%'}, status=status.HTTP_200_OK)
    except :
        return Response('Owner not found',status=status.HTTP_400_BAD_REQUEST )

# ******************************************User's Views*******************************************

# Login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
             data[k]=v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# User Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # the user should be valid
def getUserProfile(request):
    user = request.user # to get the specific user
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

# Users List
@api_view(['GET'])
@permission_classes([IsAdminUser]) # the user should be an admin only
def getUsers(request):
    user = CustomUser.objects.all() # to get the list of all users
    serializer = UserSerializerWithToken(user, many=True)
    return Response(serializer.data)

# Dashboard User Form
@api_view(['POST'])
def dashboarduser(request):
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
        user = CustomUser.objects.create(first_name=data['first_name'],last_name=data['last_name'],username=data['email'],
                                     email=data['email'],password=make_password(data['password']), is_active=False, client=client)
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
        return Response({'Message':'User Registered kindly activate ur account'})
    except:
        message = {'User Already Exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# Email Activations
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

# Clientuser Update
@api_view(['PUT'])
def edit_clientuser(request, pk, user_pk):
    client = Client.objects.get(id=pk)
    user = CustomUser.objects.get(id = user_pk)
    if request.method == 'PUT':
        user_serializer = UserSerializerWithToken(data=request.data, instance=user)
        if user_serializer.is_valid():
            user_serializer.save(client=client)
            return Response('Client User Updated')
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# DashboardUser Update
@api_view(['PUT'])
def edit_dashboardUser(requst, user_pk):
    # client = Client.objects.get(id=pk)
    user = CustomUser.objects.get(id=user_pk)
    if requst.method == 'PUT':
        user_serializr = UserSerializerWithToken(data=requst.data, instance=user)
        if user_serializr.is_valid():
            user_serializr.save()
            return Response('Dashboard User Updated')
        return Response(user_serializr.errors,status=status.HTTP_400_BAD_REQUEST)

# ClientUser Delete
@api_view(['DELETE'])
def delete_clientuser(request,pk,user_pk):
    client = Client.objects.get(id=pk)
    user = CustomUser.objects.get(id = user_pk)
    if request.method == 'DELETE':
        user.delete()
        return Response ('Client User is deleted')
    return Response ('Failed to delete Client User')

# DashboardUser Delete
@api_view(['DELETE'])
def delete_dashboarduser(request, user_pk):
    user = CustomUser.objects.get(id = user_pk)
    if request.method == 'DELETE':
        user.delete()
        return Response('Dashboard User deleted')
    return Response ('Failed to delete dashboard user')

# ******************************************Company Document **************************************

@api_view(['POST'])
def create_companydoc(request,pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        doc_serializer = CompanyDocSerailizer(data=request.data)
        if doc_serializer.is_valid():
            doc_serializer.save(client=client)
            return Response({'Message':'Company Document Created'}, status=status.HTTP_201_CREATED)
        return Response (doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_companydoc(request,pk,companydoc_pk):
    client = Client.objects.get(id=pk)
    doc = CompanyDocument.objects.get(id=companydoc_pk)
    if request.method == 'PUT':
        doc_serializer = CompanyDocSerailizer(instance=doc, data=request.data)
        if doc_serializer.is_valid():
            doc_serializer.save()
            return Response ("Document Updated")
        return Response (doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_companydoc(request,pk):
    client = Client.objects.get(id=pk)
    doc_list = CompanyDocument.objects.filter(client=client)
    serializer = CompanyDocSerailizer(doc_list,many=True)
    print(serializer)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_companydoc(request,pk,companydoc_pk):
    client = Client.objects.get(id=pk)
    doc = CompanyDocument.objects.get(id=companydoc_pk)
    if request.method == 'DELETE':
        doc.delete()
        return Response("Document Deleted")
    return Response("Failed to delete document")

# ************************************** Branch View's ********************************************

@api_view(['POST'])
def create_branch(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        branch_serializer = BranchSerailizer(data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save(client=client)
            return Response({'Message':'Branch Created'}, status=status.HTTP_201_CREATED)
        return Response(branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_branch(request,pk,branch_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id = branch_pk)
    if request.method == 'PUT':
        branch_serializer = BranchSerailizer(instance=branch, data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save(client=client)
            return Response('Branch Updated',status=status.HTTP_200_OK)
        return Response('Fail to update branch', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_branch(request,pk):
    client = Client.objects.get(id=pk)
    if request.method == 'GET':
        branch_list = Branch.objects.filter(client=client)
        branch_serializer = BranchSerailizer(branch_list, many=True)
        print(branch_serializer)
        return Response(branch_serializer.data)

@api_view(['DELETE'])
def delete_branch(request,pk,branch_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id=branch_pk)
    if request.method == 'DELETE':
        branch.delete()
        return Response ('Branch deleted')
    return Response ('Fail to delete branch')

# *************************************Office Location**********************************************

@api_view(['POST'])
def create_officelocation(request,branch_pk):
    branch = Branch.objects.get(id=branch_pk)
    if request.method == 'POST':
        officeLocation_serializer = OfficeLocationSerializer(data=request.data)
        if officeLocation_serializer.is_valid():
            officeLocation_serializer.save(branch=branch)
            return Response({'Message':'Office Location Created'}, status=status.HTTP_201_CREATED)
        return Response ('Fail to create Office Location', status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_officelocation(request,branch_pk,office_pk):
    branch = Branch.objects.get(id=branch_pk)
    office = OfficeLocation.objects.get(id=office_pk)
    if request.method == 'PUT':
        officeLocation_serializer = OfficeLocationSerializer(instance=office, data=request.data)
        if officeLocation_serializer.is_valid():
            officeLocation_serializer.save(branch=branch)
            return Response('Office Location Updated')
        return Response ('Fail to update Office Location', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_officelocation(request,pk, branch_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id = branch_pk, client=client)
    if request.method == 'GET':
        list_officelocation= OfficeLocation.objects.filter(branch=branch)
        officeLocation_serializer = OfficeLocationSerializer(list_officelocation, many=True)
        print(officeLocation_serializer)
        return Response(officeLocation_serializer.data)

@api_view(['DELETE'])
def delete_officelocation(request,pk, branch_pk, office_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id=branch_pk, client=client)
    office = OfficeLocation.objects.get(id = office_pk, branch = branch)
    if request.method == 'DELETE':
        office.delete()
        return Response('Office Location deleted')
    return Response ('Failed to delete office location', status=status.HTTP_400_BAD_REQUEST)

# *************************************Customer Or Vendor **************************************

@api_view(['POST'])
def create_customer(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        customer_serializer = CustomerVendorSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save(client=client)
            return Response({'Message':'Customer or Vendor Created'}, status=status.HTTP_201_CREATED)
        return Response ('Fail to create Customer or Vendor', status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_customer(request, pk, customer_pk):
    client = Client.objects.get(id=pk)
    customer = Customer.objects.get(id=customer_pk)
    if request.method == 'PUT':
        customer_serializer = CustomerVendorSerializer(instance=customer, data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save(client=client)
            return Response('Customer or Vendor Updated')
        return Response('Fail to update Customer or Vendor', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_customer(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'GET':
        list_customer = Customer.objects.filter(client=client)
        customer_serializer = CustomerVendorSerializer(list_customer, many=True)
        print(customer_serializer)
        return Response(customer_serializer.data)

@api_view(['DELETE'])
def delete_customer(request,pk, customer_pk):
    client = Client.objects.get(id=pk)
    customer = Customer.objects.get(id=customer_pk)
    if request.method == 'DELETE':
        customer.delete()
        return Response('Customer or Vendor deleted')
    return Response('Fail to delete Customer or Vendor')

# **********************************************Branch Document*********************************************

@api_view(['POST'])
def create_branchdoc(request,pk,branch_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id=branch_pk, client=client)
    if request.method == 'POST':
        branchdoc_serializer = BranchDocSerailizer(data=request.data)
        if branchdoc_serializer.is_valid():
            branchdoc_serializer.save(branch=branch)
            return Response({'Message':'Branch Document Created'}, status=status.HTTP_201_CREATED)
        return Response(branchdoc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_branchdoc(request,pk, branch_pk, branchdoc_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id=branch_pk, client=client)
    branchdoc = BranchDocument.objects.get(id = branchdoc_pk, branch=branch)
    if request.method == 'PUT':
        branchdoc_serializer = BranchDocSerailizer(instance=branchdoc, data=request.data)
        if branchdoc_serializer.is_valid():
            branchdoc_serializer.save(branch=branch)
            return Response('Branch Document updated')
        return Response(branchdoc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_branchdoc(request, pk, branch_pk):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id = branch_pk, client=client)
    # branchdoc = BranchDocument.objects.get(id = branchdoc_pk, branch=branch)
    if request.method == 'GET':
        list_branchdoc = BranchDocument.objects.filter(branch=branch)
        branchdoc_serializer = BranchDocSerailizer(list_branchdoc, many=True)
        print(branchdoc_serializer)
        return Response(branchdoc_serializer.data)

@api_view(['DELETE'])
def delete_branchdoc(request, pk ,branch_pk, branchdoc_pk ):
    client = Client.objects.get(id=pk)
    branch = Branch.objects.get(id = branch_pk, client=client)
    branchdoc = BranchDocument.objects.get(id = branchdoc_pk, branch=branch)
    if request.method == 'DELETE':
        branchdoc.delete()
        return Response('Branch Document Delete')
    return Response('Fail to delete branch document', status=status.HTTP_400_BAD_REQUEST)


# ***********************************************Detail page API's*********************************************
@api_view(['GET'])
def detail_client(request,pk):
    client = Client.objects.get(id=pk)
    view_bank = Bank.objects.filter(client=client)
    view_owner = Owner.objects.filter(client=client)
    view_clientuser = CustomUser.objects.filter(client=client)
    view_companydoc = CompanyDocument.objects.filter(client=client)
    view_branch = Branch.objects.filter(client=client)
    view_customer = Customer.objects.filter(client=client)
    # view_branchdoc = BranchDocument.objects.filter()


    client_serializer = ClientSerializer(client)
    bank_serializer = BankSerializer(view_bank, many=True)
    owner_serializer = OwnerSerializer(view_owner, many=True)
    clientuser = UserSerializerWithToken(view_clientuser, many=True)
    companydoc = CompanyDocSerailizer(view_companydoc, many=True)
    branch_serializer = BranchSerailizer(view_branch, many=True)
    customer_serializer = CustomerVendorSerializer(view_customer, many=True)



    data ={
        'Client' : client_serializer.data,
        'Bank' : bank_serializer.data,
        'Owner' : owner_serializer.data,
        'ClientUser' : clientuser.data,
        'Company Document' : companydoc.data,
        'Branch' : branch_serializer.data,
        'Customer or Vendor' : customer_serializer.data
    }
    return Response(data)

@api_view(['GET'])
def detail_branch(request, pk, branch_pk):
    client = Client.objects.get(id = pk)
    branch = Branch.objects.get(id = branch_pk, client=client)
    officeloaction = OfficeLocation.objects.filter(branch = branch)
    view_branchdoc = BranchDocument.objects.filter(branch=branch)

    branch_serializer = BranchSerailizer(branch)
    officeloaction_serializer = OfficeLocationSerializer(officeloaction, many=True)
    branchdoc_serializer = BranchDocSerailizer(view_branchdoc, many=True)

    data = {
        'Client Name' :client.client_name, # to only retrive client name
        'Branch' : branch_serializer.data,
        'Office Location' : officeloaction_serializer.data,
        'Branch Document' : branchdoc_serializer.data,
    }
    return Response(data)


