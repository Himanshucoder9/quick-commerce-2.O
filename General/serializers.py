from rest_framework import serializers
from General.models import SiteConfig, State, City, Country, SocialMedia, About, PrivacyPolicy, TermsAndCondition, \
    FAQCategory, FAQ, Contact, Feedback


# Country
class FullCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code",)


# State
class FullStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "name", "code", "is_available",)


# City
class FullCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "state", "is_available",)


class SimpleCitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "state", "is_available",)


# SiteConfig

class FullSiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = "__all__"


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = (
            "id", "title", "favicon", "logo", "email", "primary_mobile", "secondary_mobile", "address",
            "short_description", "playstore", "appstore")


# SocialMedia

class FullSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ("id", "site_config", "name", "url",)


# About

class FullAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ("id", "title", "description", "created_at", "updated_at")


# PrivacyPolicy

class FullPrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ("id", "title", "description", "created_at", "updated_at")


# TermsAndCondition

class FullTermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = "__all__"


class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = ("id", "title", "description", "created_at", "updated_at")


# FAQCategory

class FullFAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = "__all__"


class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = ("id", "title",)


# FAQ
class FullFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "category",)


class SimpleFAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "category", "created_at", "updated_at")


# Contact
class FullContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name", "email", "mobile", "subject", "message", "created_at", "updated_at")


# Feedback
class FullFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("name", "message", "rating", "created_at", "updated_at")
