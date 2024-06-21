from django.urls import path
from apps.users import views


app_name = 'users'

urlpatterns = [
    # Register page
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # Success register
    path('register/success/', views.RegistrationSuccessView.as_view(), name='register_success'),
    # Verify email
    path('verify/<uuid:uuid>/', views.RegistrationVerifyView.as_view(), name='verify'),
    # Success verify
    path('verify/success/', views.VerificationSuccessView.as_view(), name='verify_success'),
    # Login
    path('login/', views.LoginView.as_view(), name='login'),
    # Logout
    path('logout/', views.logout_view, name='logout'),
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # Profiles
    path('profiles/list/', views.ProfilesView.as_view(), name='profiles'),
    path('profiles/create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profiles/update/<uuid:uuid>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profiles/view/<uuid:uuid>/', views.ProfileDetailView.as_view(), name='view_profile'),
    # Emergency contacts
    path('emergency-contacts/list/', views.EmergencyContactsView.as_view(), name='emergency_contacts'),
    path('emergency-contacts/create/', views.CreateEmergencyContactView.as_view(), name='create_emergency_contact'),
    path('emergency-contacts/update/<uuid:uuid>/', views.UpdateEmergencyContactView.as_view(), name='update_emergency_contact'),
    path('emergency-contact/view/<uuid:uuid>/', views.EmergencyContactListView.as_view(), name='view_emergency_contact'),
    # User methods API
    path('methods/change-password/', views.change_password, name='change_password_api'),
    # Change password
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    # Terms and conditions 
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions_api'),
    # Faqs
    path('faqs/', views.FaqView.as_view(), name='faqs')
]