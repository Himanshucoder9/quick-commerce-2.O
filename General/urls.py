from django.urls import path
from General.views import (
    CountryListView,
    StateListView,
    CityListView,
    SiteConfigView,
    SocialMediaList,
    AboutView,
    PrivacyPolicyView,
    TermsAndConditionView,
    ContactCreateView,
    FeedbackCreateView,
    FAQListView,
)

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('states/', StateListView.as_view(), name='state-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('site-config/', SiteConfigView.as_view(), name='site-config'),
    path('social-media/', SocialMediaList.as_view(), name='social-media-list'),
    path('about-us/', AboutView.as_view(), name='about-us'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionView.as_view(), name='terms-and-conditions'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
]
