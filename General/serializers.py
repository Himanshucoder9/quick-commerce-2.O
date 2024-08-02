from rest_framework import serializers
from General.models import (
    SiteConfig, State, City, Country, SocialMedia,
    About, PrivacyPolicy, TermsAndCondition, FAQCategory,
    FAQ, Contact, Feedback
)


# Country Serializers
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code",)


class FullCountrySerializer(CountrySerializer):
    class Meta(CountrySerializer.Meta):
        fields = "__all__"


# State Serializers
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "name", "abbreviation", "is_available",)


class FullStateSerializer(StateSerializer):
    class Meta(StateSerializer.Meta):
        fields = "__all__"


# City Serializers
class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = ("id", "name", "state", "is_available",)


class FullCitySerializer(CitySerializer):
    class Meta(CitySerializer.Meta):
        fields = "__all__"


# SiteConfig Serializers
class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = (
            "id", "title", "favicon", "logo", "email",
            "primary_mobile", "secondary_mobile", "address",
            "short_description", "playstore", "appstore"
        )


class FullSiteConfigSerializer(SiteConfigSerializer):
    class Meta(SiteConfigSerializer.Meta):
        fields = "__all__"


# SocialMedia Serializers
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ("id", "site_config", "name", "url",)


class FullSocialMediaSerializer(SocialMediaSerializer):
    class Meta(SocialMediaSerializer.Meta):
        fields = "__all__"


# About Serializers
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ("id", "title", "description", "created_at", "updated_at",)


class FullAboutSerializer(AboutSerializer):
    class Meta(AboutSerializer.Meta):
        fields = "__all__"


# PrivacyPolicy Serializers
class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ("id", "title", "description", "created_at", "updated_at",)


class FullPrivacyPolicySerializer(PrivacyPolicySerializer):
    class Meta(PrivacyPolicySerializer.Meta):
        fields = "__all__"


# TermsAndCondition Serializers
class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = ("id", "title", "description", "created_at", "updated_at",)


class FullTermsAndConditionSerializer(TermsAndConditionSerializer):
    class Meta(TermsAndConditionSerializer.Meta):
        fields = "__all__"


# FAQCategory Serializers
class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = ("id", "title",)


class FullFAQCategorySerializer(FAQCategorySerializer):
    class Meta(FAQCategorySerializer.Meta):
        fields = "__all__"


# FAQ Serializers
class FAQSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer()

    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "category",)


class FullFAQSerializer(FAQSerializer):
    class Meta(FAQSerializer.Meta):
        fields = "__all__"


# Contact Serializers
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name", "email", "mobile", "subject", "message", "created_at", "updated_at",)


class FullContactSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        fields = "__all__"


# Feedback Serializers
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("name", "message", "rating", "created_at", "updated_at",)


class FullFeedbackSerializer(FeedbackSerializer):
    class Meta(FeedbackSerializer.Meta):
        fields = "__all__"
