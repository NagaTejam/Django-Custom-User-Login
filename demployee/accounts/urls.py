from django.urls import path,include
from .import views


urlpatterns = [
	path('',views.home,name='home'),
	path('signup/',views.register,name='signup'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.user_logout,  name='logout'),
	path('profile/', views.view_profile,  name='view_profile'),
	path('profile/edit/',views.edit_profile, name='edit_profile'),
	path('change_password/', views.change_password, name='change_password'),
	path('profile/service/', views.service, name='service'),
	path('delete/<emp_id>', views.destroy, name='delete'),
	path('edit/<emp_id>', views.edit, name='edit'),
	path('profile/admin/',views.admin,name='admin')
]