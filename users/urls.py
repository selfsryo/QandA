from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views as my_views


app_name = 'users'

urlpatterns = [
    path('detail/<str:username>/', my_views.UserDetailView.as_view(), name='user_detail'),
    path('signup/', my_views.UserSignUpView.as_view(), name='signup'),
    path('update/<str:username>/', my_views.UserUpdateView.as_view(), name='user_update'),
    path('follow/<str:username>/', my_views.UserFollow.as_view(), name='user_follow'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password/', my_views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
                                                                              name='password_change_done'),

    path('password_reset/', my_views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
                                                                                   name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', my_views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
                                                                                           name='password_reset_complete'),
]
