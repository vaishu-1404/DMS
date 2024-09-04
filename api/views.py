from urllib import request
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import *
from api.serializers import *


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_client(request):
    instance_data = request.data
    data = {key: value for key, value in instance_data.items()}

    # Serialize the client data
    serializer = ClientSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        client_instance = serializer.save()

        # Handle file uploads
        if request.FILES:
            files = dict((request.FILES).lists()).get('files', None)
            if files:
                for file in files:
                    file_data = {
                        "client": client_instance.pk,
                        "files": file
                    }
                    file_serializer = FileSerializer(data=file_data)
                    if file_serializer.is_valid(raise_exception=True):
                        file_serializer.save()

        # Return the response with the client data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ClientViewSet(viewsets.ModelViewSet):
#     serializer_class = ClientSerializer
#     queryset = Client.objects.all()
#     parser_classes = [MultiPartParser, FormParser]

#     def create(self, request, *args, **kwargs):
#         instance_data = request.data
#         data = {key: value for  key, value in instance_data.items()}
#         serializers = self.get_serializer(data=data)
#         serializers.is_valid(raise_exception=True)
#         instance = serializers.save()

#         if request.FILES:
#             files = dict((request.FILES).lists()).get('files',None)
#             if files:
#                 for file in files:
#                     file_data = {}
#                     file_data["client"] = instance.pk
#                     file_data["files"] = file
#                     file_serializer = FileSerializer(data=file_data)
#                     file_serializer.is_valid(raise_exception=True)
#                     file_serializer.save()
#         return Response(serializers.data)

@api_view(['DELETE'])
def delete_client(request,pk):
    if request.method == 'DELETE':
        client = Client.objects.get(id=pk)
        client.delete()
        return Response ('Company Deleted')
    return Response ('Fail to delete')
    # try:
    #     client = Client.objects.get(pk=pk)
    #     client.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    # except Client.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_client(request):
    if request.method == 'GET':
        client = Client.objects.all()
        serializers = ClientSerializer(client, many=True)
        return Response(serializers.data)


# class HandleFileUpload(APIView):

#     def post(self, request):
#         try:
#             data = request.data
#             serializers = FileListSerializer(data=data)
#             if serializers.is_valid():
#                 serializers.save()
#                 return Response("File Uploaded", status=status.HTTP_200_OK)
#             return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#         except UnsupportedMediaType as e:
#             return Response({"error": "Unsupported media type", "details": str(e)}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
#         except Exception as e:
#             print(e)
#             return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class HandleFileUpload(APIView):

#     def post(self, request):
#         try:
#             data = request.data
#             serializers = FileListSerializer(data=data)
#             if serializers.is_valid():
#                 serializers.save()
#                 return Response("File Uploded", status=status.HTTP_200_OK)
#             return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(e)
# Create your views here.
# @api_view(['POST'])
# def multiple_upload(request):
#     mom = request.FILES.getlist("mom")

#     mom_list = []
#     for i in mom:
#         mom_list.append(ClientFile(mom=i))

#     if mom_list:
#         ClientFile.objects.bulk_create(mom_list)
#     return Response("done")

# @api_view(['POST'])
# def create_owner(request):
#     if request.method == 'POST':

# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def create_client(request):
#         if 'mom' in request.FILES:
#             mom = request.FILES.getlist('mom')
#             document_instances = [ClientFile(file=doc) for doc in mom]
#             ClientFile.objects.bulk_create(document_instances)

#         serializer = ClientSerializer(data=request.data, context={'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser, JSONParser)

#     def post(self, request, *args, **kwargs):
#         files = request.FILES.getlist('files')
#         serializer = ClientSerializer(data= request.data)
#         print('iless',files)

#         if serializer.is_valid():
#             client = serializer.save()
#             for i in files:
#                 category = request.data.get('file_category')
#                 ClientFile.objects.create(files=i, client=client, file_category=category)
#             return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)
#         else:
#              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     client = Client.objects.all()
    #     serializers = ClientSerializer(client, many=True)

    #     return Response(serializers.data)

    # def post(self, request, format=None):
    #     serializer = FileListSerializer(data= request.data)
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(serializers.data, status=status.HTTP_201_CREATED)
    #     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
