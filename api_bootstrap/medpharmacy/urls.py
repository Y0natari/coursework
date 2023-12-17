from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drug_inventory.views import DrugViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'drugs', DrugViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
