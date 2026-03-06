from django.urls import path


from .views import sign_v,login_v,logout_v,home_v,blog1,blog2,blog3,blog4,my_saved_recipes

urlpatterns=[
    path('', home_v, name='home'),
    path("signup/",sign_v,name="signup"),
    path("login/",login_v,name="login"),
    path('logout/',logout_v,name="logout"),
    path('blog1/', blog1, name='blog1'),
    path('blog2/', blog2, name='blog2'),
    path('blog3/', blog3, name='blog3'),
    path('blog4/',blog4, name='blog4'),
    path("saved-recipes/",my_saved_recipes,
     name="my_saved_recipes"),



]