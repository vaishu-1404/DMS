from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from api.models import *
from api.serializers import *

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

@api_view(['DELETE'])
def delete_client(request,pk):
    if request.method == 'DELETE':
        client = Client.objects.get(id=pk)
        client.delete()
        return Response ('Company Deleted')
    return Response ('Fail to delete')



