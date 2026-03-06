from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.recipe_generator_view, name='recipe_generator'),
    path("my_recipes/", views.my_recipes, name="saved_recipes"),
    
    path("shoppinglist/",views.shopping_list_view,name="shopping_list"),
    path('delete-recipe/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    path('health-supporter/', views.health_supporter_view, name='health_supporter'),

]
