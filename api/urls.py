from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('api/vendor',VendorViewset,basename='vendor')
router.register('api/purchase_orders',PurchaseOrderViewset,basename='purchase_orders')
urlpatterns =router.urls