from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from api.models import *
from api.serializers import *


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

    client_serializer = ClientSerializer(client)
    bank_serializer = BankSerializer(view_bank, many=True)
    owner_serializer = OwnerSerializer(view_owner, many=True)

    data ={
        'client' : client_serializer.data,
        'bank' : bank_serializer.data,
        'owner' : owner_serializer.data
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






