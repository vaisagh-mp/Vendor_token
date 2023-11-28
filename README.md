# Vendor-Management-System
  This document provides details about the API endpoints available in the Vendor Management System.

Base URL
The base URL for all API endpoints.
{
    "api/vendor": "http://127.0.0.1:8000/api/vendor/",
    "api/purchase_orders": "http://127.0.0.1:8000/api/purchase_orders/"
}

Endpoints

#############################################################################################

VENDORS:

List all Vendors
  GET /vendors/
  Retrieves a list of all vendors.
  
Retrieve a specific vendor's details
  GET /vendors/{vendor_id}/
  Retrieves details of a specific vendor identified by {vendor_id}.
  
Add new Vendor
  POST /vendors/
  Adds a new vendor.
  
Edit Vendor
  PUT /vendors/{vendor_id}/
  Modifies details of the vendor identified by {vendor_id}.
  
Delete Vendor
  DELETE /vendors/{vendor_id}/
  Deletes the vendor identified by {vendor_id}.
  
Retrieves the calculated performance metrics for a specific vendor
  GET /vendors/{vendor_id}/performance
  Retrieves performance metrics for the vendor identified by {vendor_id}.

#################################################################################################

PURCHASE ORDERS : 

List all Purchase Orders
  GET /purchase_orders/
  Retrieves a list of all purchase orders.
  
Retrieve details of a specific purchase order
  GET /purchase_orders/{po_id}/
  Retrieves details of a specific purchase order identified by {po_id}.
  
Add new Purchase Order
  POST /purchase_orders/
  Adds a new purchase order.
  
Edit Purchase Order
  PUT /purchase_orders/{po_id}/
  Modifies details of the purchase order identified by {po_id}.
  
Delete Purchase Order
  DELETE /purchase_orders/{po_id}/
  Deletes the purchase order identified by {po_id}.
  
Update acknowledgment_date and trigger recalculation of average_response_time
  PATCH /purchase_orders/{po_id}/acknowledge
  Updates the acknowledgment_date of the purchase order identified by {po_id} and triggers recalculation of average_response_time.





  
