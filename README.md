# Vendor-Management-System-with-Performance-Metrics

Hello sir, this the assignment of Vendor Management System with performance Metric Calculation

There are some steps needed to follow while processing the application

1. Clone this repository using this command "git clone https://github.com/nitin1053/Vendor-Management-System-with-Performance-Metrics.git".

2. Navigate through the project and run the command "pip install -r requirements.txt" in your terminal.

3. After that run the django project in your terminal "python3 manage.py runserver" .

To get the swagger api documentation
URL:- http://127.0.0.1:8000/api/swagger/

Now as let see all the apis and there working,
Firstly generate a acces token using:-



Signup
URL: http://127.0.0.1:8000/api/signup/
Method: POST
JSON
{
    "username": "Rahul",
    "email": "testuser@example.com",
    "password": "1234567"
}

Now after that do login

Login
URL: http://127.0.0.1:8000/api/login/
Method: POST
JSON
{
  "username": "Rahul",
  "password": "1234567"
}

Copy the acces token in the response

Click on authorization select "Bearer token" and paste the acces token got from login to the box aside the bearer token. Do this for  all the apis


Vendor List/Create API:
URL: http://127.0.0.1:8000/api/vendors/To get the swagger api
URL:- http://127.0.0.1:8000/api/swagger/
Method: POST
JSON in BODY--> 
{
    "name": "Vendor Name",
    "contact_details": "Vendor Contact Details",
    "address": "Vendor Address",
    "vendor_code": "12345"
}

Vendor List/Create API:
URL: http://127.0.0.1:8000/api/vendors/
Method: GET
--> To reterive all the detail of the vendors

To do CRUD operation;
VendorDetailAPIView
URL: http://127.0.0.1:8000/api/vendors/{id} #get the id from json response
Method:- get,update,delete,post



Purchase Order List/Create API:
URL: http://127.0.0.1:8000/api/purchase_orders/
Method: POST
JSON in body
{
    "po_number": "PO123",
    "vendor": 1,  # Replace with the ID of an existing vendor
    "order_date": "2024-05-03",
    "delivery_date": "2024-05-10",
    "items": "Item 1",
    "quantity": 10,
    "status": "completed",
    "quality_rating": 4,
    "issue_date": "2024-05-03",
    "acknowledgment_date": "2024-05-03"
}

Purchase Order List/Create API:
URL: http://127.0.0.1:8000/api/purchase_orders/
Method: GET
--> TO reterive all the purchase orders


PurchaseOrderDetailAPIView
URL: http://127.0.0.1:8000/api/purchase_orders/{po_number} get the po_number from json response 
Perform all the CRUD operation in proper way.
Method:- get,update,delete,post

VendorPerformanceAPIView
URL:- [vendors/<int:vendor_id>/performance/](http://127.0.0.1:8000/api/vendors/1/performance/)
METHOD:-GET
--> to get the vendors peformance




