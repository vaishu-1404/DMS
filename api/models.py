from django.db import models
import os

# Create your models here.

#Owner Model
class Owner(models.Model):
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    share = models.IntegerField(default=100, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    it_password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.owner_name

# Bank Model
class Bank(models.Model):
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.IntegerField(null=True, blank=True)
    ifsc = models.CharField(max_length=50, null=True, blank=True)
    account_type = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.bank_name

# Client Model
class Client(models.Model):

    entites = [
       ('proprietorship','Proprietorship'),
       ('partnership', 'Partnership'),
       ('llp', 'LLP'),
       ('opc', 'OPC'),
       ('huf', 'HUF'),
       ('private ltd', 'Private Ltd'),
       ('Public Limited', 'public limited'),
       ('trust', 'Trust')
    ]

    client_name = models.CharField(max_length=100, null=True, blank=True)
    entity_type = models.CharField(max_length=100, choices=entites, null=True, blank=True)
    date_of_incorporation = models.DateField(null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    contact_no_1 = models.IntegerField(null=True, blank=True)
    contact_no_2 = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    business_detail = models.TextField(null=True, blank=True)
    # mom = models.ManyToManyField(ClientFile, related_name="client")
    # pf = models.FileField(upload_to='pf/',null=True, blank=True)
    # owner = models.ManyToManyField(Owner, related_name='Client', blank=True)
    # bank = models.ManyToManyField(Bank, related_name='Client', blank=True)

    def __str__(self):
        return self.client_name  if self.client_name else 'No name provided'

#File
class File(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    files = models.FileField(upload_to='files')

#User Model
class User(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    ca_admin = models.BooleanField(null=True, blank=True)
    ca_user = models.BooleanField(null=True, blank=True)
    cus_admin = models.BooleanField(null=True, blank=True)
    cus_user = models.BooleanField(null=True, blank=True)
    company = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)

#Branch Model
class Branch(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    gst_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.branch_name

#OfficeLocation Model
class OfficeLocation(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.location

#Customer or Vendor Model
class Customer(models.Model):

   type_choices = [
         ('customer', 'Customer'),
         ('vendor', 'Vendor'),
     ]
   name = models.CharField(max_length=100, null=True, blank=True)
   gst_no = models.CharField(max_length=100, null=True, blank=True)
   pan = models.CharField(max_length=100, null=True, blank=True)
   address = models.TextField(null=True, blank=True)
   type = models.CharField(max_length=100, choices=type_choices, null=True, blank=True)
   client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
   customer = models.BooleanField(null=True, blank=True)
   vendor = models.BooleanField(null=True, blank=True)

   def __str__(self):
        return self.name

#HSN Code Model
class HSNCode(models.Model):
    hsn_code = models.IntegerField(null=True, blank=True)
    gst_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#Sales Invoice Model
class SalesInvoice(models.Model):

    invoice_type = [
        ('B2B', 'Business to Business'),
        ('B2C-L', 'Business to Consumer -Local'),
        ('BSC-O', 'BSC- Other'),
        ('Nil Rated', 'Nil Rated'),
        ('Advance Received', 'Advance Received'),
        ('Export', 'Export'),
        ('Unregistered local', 'Unregistered Local'),
    ]

    entry_type = [
        ('sales_invoice', 'Sales_Invoice'),
        ('debit_note', 'Debit Note'),
        ('income', 'Income'),
    ]
    client_Location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True, blank=True)
    attach_invoice = models.FileField(null=True, blank=True)
    attach_e_way_bill = models.FileField(null=True, blank=True)
    month = models.DateField(null=True, blank=True)
    cutomer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    invoice_no = models.CharField(max_length=100, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_type = models.CharField(max_length=100, choices=invoice_type, null=True, blank=True)
    entry_type = models.CharField(max_length=100, choices=entry_type, null=True, blank=True)
    hsn = models.ForeignKey(HSNCode, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=100, null=True, blank=True)
    unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_invoice_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tds_tcs_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tds_tcs_section = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tcs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tds = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_receivable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#Purchase Invoice Model
class PurchaseInvoice(models.Model):
   entry_type = [
        ('purchase_invoice', 'Purchase_Invoice'),
        ('credit_note', 'Credit Note'),
        ('expenses', 'Expenses'),
    ]
   client_Location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True, blank=True)
   attach_invoice = models.FileField(null=True, blank=True)
   attach_e_way_bill = models.FileField(null=True, blank=True)
   utilise_credit = models.BooleanField(null=True, blank=True)
   month = models.DateField(null=True, blank=True)
   vendor = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
   invoice_no = models.CharField(max_length=100, null=True, blank=True)
   invoice_date = models.DateField(null=True, blank=True)
   entry_type = models.CharField(max_length=100, choices=entry_type, null=True, blank=True)
   hsn = models.ForeignKey(HSNCode, on_delete=models.CASCADE, null=True, blank=True)
   description = models.TextField(null=True, blank=True)
   unit_of_measure = models.CharField(max_length=100, null=True, blank=True)
   unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   total_invoice_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   tds_tcs_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   tds_tcs_section = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   tcs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   tds = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   amount_receivable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

# CompanyDocument Model
class CompanyDocument(models.Model):

    document_type = [
        ('Pan', 'PAN'),
        ('tan', 'TAN'),
        ('msme','MSME'),
        ('udym', 'UDYM'),
        ('mca', 'MCA'),
        ('pf', 'PF'),
        ('esic', 'ESIC'),
        ('other', 'OTHER'),
    ]
    company = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    document_type = models.CharField(max_length=100, choices=document_type, null=True, blank=True)
    login = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

# Branch Document Model
class BranchDocument(models.Model):
    document_type = [
        ('ptec', 'PTEC'),
        ('ptrc', 'PTRC'),
        ('gst', 'GST'),
        ('eway', 'EWAY'),
        ('other', 'OTHER'),
    ]
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    document_type = models.CharField(max_length=100, choices=document_type, null=True, blank=True)
    login = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)


