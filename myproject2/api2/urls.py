from django.urls import path
from .views import SignupView, LoginView, FileUploadView
from .views import UserDetailView, UserListView, UserUpdateView

urlpatterns = [
    path('user/signup/', SignupView.as_view(), name='signup'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/upload/', FileUploadView.as_view(), name='upload'),
    path('user/view/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
]
