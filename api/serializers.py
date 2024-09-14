from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import *
from rest_framework_simplejwt.tokens import RefreshToken

# File Serializer

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']

# Client Serializer

class ClientSerializer(serializers.ModelSerializer):
    mom = serializers.SerializerMethodField()
    pf = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id','client_name','entity_type','date_of_incorporation','contact_person','designation','contact_no_1','contact_no_2','email','business_detail','mom','pf']

    def get_mom(self, obj):
        return FileSerializer(obj.mom.all(), many=True).data

    def get_pf(self, obj):
        return FileSerializer(obj.pf.all(), many=True).data

    def create(self, validated_data):
        mom_files = self.context['request'].FILES.getlist('mom')
        pf_files = self.context['request'].FILES.getlist('pf')

        file_instance = Client.objects.create(
            client_name=validated_data.get('client_name'),
            entity_type=validated_data.get('entity_type'),
            date_of_incorporation=validated_data.get('date_of_incorporation'),
            contact_person=validated_data.get('contact_person'),
            designation=validated_data.get('designation'),
            contact_no_1=validated_data.get('contact_no_1'),
            contact_no_2=validated_data.get('contact_no_2'),
            email=validated_data.get('email'),
            business_detail=validated_data.get('business_detail'),
        )

        # Handle mom files
        for mom_file in mom_files:
            uploaded_file = File.objects.create(file=mom_file)
            file_instance.mom.add(uploaded_file)

        # Handle pf files
        for pf_file in pf_files:
            uploaded_file = File.objects.create(file=pf_file)
            file_instance.pf.add(uploaded_file)

        return file_instance

# Bank Serializer
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

# Owner Serializer
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

# User Serializer
class UserSerializerWithToken(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only= True)
    token = serializers.SerializerMethodField(read_only = True)
    ca_admin = serializers.SerializerMethodField()
    cus_admin = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','username','email','name','first_name','last_name','ca_admin', 'cus_admin', 'token','client']

    def get_name(self, obj):
        firstname = obj.first_name
        lastname = obj.last_name
        name = firstname + ' ' + lastname
        if name==' ':
            name = 'Set Your Name'
        return name

    def get_ca_admin(self,obj):
        return obj.is_staff

    def get_cus_admin(self, obj):
        return obj.is_staff

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


# Company Document
class CompanyDocSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDocument
        fields ='__all__'

# Branch
class BranchSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

# Office Location
class OfficeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = '__all__'

# Branch Document
class BranchDocSerailizer(serializers.ModelSerializer):
    class Meta:
        model = BranchDocument
        fields = '__all__'

# Customer Or Vendor
class CustomerVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Incometax Document
class IncomeTaxDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTaxDocument
        fields = '__all__'

# PF
class PfSerializer(serializers.ModelSerializer):
    class Meta:
        model = PF
        fields = '__all__'
