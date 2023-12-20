from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
   path('',views.landing,name='landing'),
   path('signup/', views.signup, name='signup'),
   path('activate/<uidb64>/<token>', views.activate, name='activate'),
   path('signin', views.signin, name='signin'),
   path('signout', views.signout, name='signout'),
   path('home/',views.home,name="home"),
   path('about/',views.about,name="about"),
    #path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
   # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
   # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
   # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    

]
