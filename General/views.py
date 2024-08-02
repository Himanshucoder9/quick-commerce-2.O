from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from General.models import (
    Country,
    State,
    City,
    SiteConfig,
    SocialMedia,
    About,
    PrivacyPolicy,
    TermsAndCondition,
    FAQ,
    Contact,
    Feedback,
)
from General.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    SiteConfigSerializer,
    SocialMediaSerializer,
    AboutSerializer,
    PrivacyPolicySerializer,
    TermsAndConditionSerializer,
    FAQSerializer,
    ContactSerializer,
    FeedbackSerializer,
)


class BaseListView(ListAPIView):
    """Base class for list views with available filter."""
    def get_queryset(self):
        """Override to filter available objects."""
        return self.queryset.filter(is_available=True) if hasattr(self.queryset.model, 'is_available') else self.queryset


class CountryListView(BaseListView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateListView(BaseListView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'states': serializer.data}, status=status.HTTP_200_OK)


class CityListView(BaseListView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'cities': serializer.data}, status=status.HTTP_200_OK)


class BaseRetrieveView(RetrieveAPIView):
    """Base class for retrieving the latest object."""
    def get_object(self):
        """Get the latest object of the model."""
        try:
            return self.queryset.latest('created_at')
        except self.queryset.model.DoesNotExist:
            raise Http404(f"No {self.queryset.model.__name__.lower()} found")


class SiteConfigView(BaseRetrieveView):
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer


class SocialMediaList(BaseListView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer


class AboutView(BaseRetrieveView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class PrivacyPolicyView(BaseRetrieveView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


class TermsAndConditionView(BaseRetrieveView):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer


class FAQListView(BaseListView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class ContactCreateView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class FeedbackCreateView(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
