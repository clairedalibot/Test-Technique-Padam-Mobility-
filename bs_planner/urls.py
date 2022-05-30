from django.urls import path
from .views import index, delete_bs, add_bs

urlpatterns = [
    path('', index, name='bs_planner-index'),
    path('delete_bs/', delete_bs, name='delete_bs'),
    path('add_bs/', add_bs, name='add_bs')
]