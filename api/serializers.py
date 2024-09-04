# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import *

# client

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id','client_name','entity_type','date_of_incorporation','contact_person','designation','contact_no_1','contact_no_2','email','business_detail','files']

    def get_files(self, obj):
        files = File.objects.filter(client=obj)
        return FileSerializer(files, many=True, read_only = False).data

    # class Meta:
    #     model = Client
    #     fields = ['files','client_name','entity_type']


# class FileListSerializer(serializers.ModelSerializer):

#     parser_classes = [MultiPartParser, FormParser]

#     files = serializers.ListField(
#         child = serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False)
#     )

#     class Meta:
#         model = File
#         fields = '__all__'

#     def create(self, validated_data):
#         client = Client.objects.create()
#         files = validated_data.pop('files')
#         files_obj =[]
#         for file in files:
#             files_obj = File.objects.create(client=client, files=file)
#             files_obj.append(files_obj)
#         return files_obj

#     mom = serializers.ListField(
#         child=serializers.FileField(max_length=10000,
#                                     allow_empty_file=False,
#                                     use_url=False)
#     )
#     # class Meta:
#     #     model = Client
#     #     fields = '__all__'
#     def create(self,validated_data):
#         mom = validated_data.pop('mom')
#         for file in mom:
#             f = Client.objects.create(mom=file,**validated_data)
#         return f

# class ClientFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientFile
#         fields = ['mom']

# class ClientSerializer(serializers.ModelSerializer):
#     mom = ClientFileSerializer(many=True, required=False)

#     class Meta:
#         model = Client
#         fields = '__all__'

#     def create(self, validated_data):
#         data = validated_data.pop('mom')
#         # data = self.context['request'].FILES.getlist('mom')
#         client = Client.objects.create(**validated_data)
#         for data in data:
#             ClientFile.objects.create(client=client, **data)
#         return client
