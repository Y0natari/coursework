from rest_framework import viewsets
from .models import Drug, Category
from .serializers import DrugSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        category_id = self.request.query_params.get('id', None)
        if category_id is not None:
            queryset = queryset.filter(id=category_id)
        return queryset

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    def get_queryset(self):
        queryset = Drug.objects.all()
        drug_id = self.request.query_params.get('id', None)
        category_id = self.request.query_params.get('category_id', None)
        if drug_id is not None:
            queryset = queryset.filter(id=drug_id)
        elif category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
