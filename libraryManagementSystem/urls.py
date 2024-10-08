"""
URL configuration for libraryManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/add/', BookAddView.as_view(), name='book-add'), #[revisit]
    path('books/<int:book_id>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:book_id>/update/', BookUpdateView.as_view(), name='book-update'), #[revisit]

    path('books/<int:book_id>/copies/add/', BookCopyAddView.as_view(), name='book-copy-add'), #[revisit]
    path('books/<int:book_id>/copies/<int:copy_id>/delete/', BookCopyDeleteView.as_view(), name='book-copy-delete'), #[revisit]

    # path('users/members/', MemberListView.as_view(), name='member-list'),
    path('users/add/', UserAddView.as_view(), name='user-add'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:user_id>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/active/', ActiveUserListView.as_view(), name='user-active-list'),

    path('user/<int:user_id>/history/', UserHistoryView.as_view(), name='user-history'),
    path('book/issue/', BookIssueView.as_view(), name='book-issue'),
    path('book/<int:transaction_id>/return/', BookReturnView.as_view(), name='book-return'),
]
