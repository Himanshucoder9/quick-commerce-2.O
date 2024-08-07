from django.contrib import admin
from django.utils.html import format_html, strip_tags
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Country Info', {
            'fields': (
                'name', 'code',),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ['name', 'code', 'created_at']
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name', 'code',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(State)
class StateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('State Info', {
            'fields': (
                'name', 'code', 'is_available'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ['name', 'code', 'is_available', 'created_at']
    list_filter = ('is_available', 'created_at', 'updated_at',)
    search_fields = ('name', 'code',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('City Info', {
            'fields': (
                'name', 'state', 'is_available'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ['name', 'state', 'is_available', 'created_at']
    list_filter = ('is_available', 'created_at', 'updated_at',)
    search_fields = ('name', 'code',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(SiteConfig)
class SiteConfigAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Site Info', {
            'fields': (
                'title', 'logo', 'favicon', 'short_description', 'primary_mobile', 'secondary_mobile', 'email',
                'address', 'playstore', 'appstore'),
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.logo.url))
        else:
            return "No Logo"

    _logo.short_description = "Logo"

    list_display = ['title', '_logo', 'primary_mobile', 'email', 'address', ]
    list_filter = ('title', 'email', 'primary_mobile', 'created_at', 'updated_at',)
    search_fields = ('title', 'primary_mobile', 'email',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(SocialMedia)
class SocialMediaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Social Media', {
            'fields': (
                'name', 'url',),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ['name', 'url', ]
    list_filter = ['name', ]
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 15


@admin.register(About)
class AboutAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('About Info', {
            'fields': ('title', 'description',),
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def truncated_description(self, obj):
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''

    truncated_description.short_description = 'Description'

    list_display = ['title', 'truncated_description', 'created_at', 'updated_at', ]
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title', 'description',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 10


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Privacy Policy Info', {
            'fields': ('title', 'description',),
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def truncated_description(self, obj):
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''

    truncated_description.short_description = 'Description'

    list_display = ['title', 'truncated_description', 'created_at', 'updated_at', ]
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title', 'description',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 10


@admin.register(TermsAndCondition)
class TermsAndConditionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Terms & Condition Info', {
            'fields': ('title', 'description',), }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def truncated_description(self, obj):
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''

    truncated_description.short_description = 'Description'

    list_display = ['title', 'truncated_description', 'created_at', 'updated_at', ]
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title', 'description',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 10


@admin.register(FAQ)
class FAQAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('FAQ Info', {
            'fields': ('category', 'question', 'answer',),
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _answer(self, obj):
        return strip_tags(obj.answer)[:50] + '...' if obj.answer else ''

    _answer.short_description = 'Answer'

    list_display = ['id', 'category', 'question', '_answer', 'created_at', 'updated_at', ]
    list_filter = ('category', 'question', 'created_at', 'updated_at',)
    search_fields = ('question', 'category')
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 10


@admin.register(FAQCategory)
class FAQCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('FAQ Category Info', {
            'fields': ('title',),
        }),

        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'canonical'),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ['title', 'created_at', 'updated_at', ]
    list_filter = ('title', 'created_at', 'updated_at',)
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at',)
    list_per_page = 10


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'mobile', 'subject', 'message',),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def has_add_permission(self, request):
        return False

    list_display = ['name', 'email', 'mobile', 'subject', 'message', ]
    list_filter = ('name', 'email', 'created_at', 'updated_at',)
    search_fields = ('name', 'email', 'mobile',)
    readonly_fields = ('name', 'email', 'mobile', 'subject', 'message', 'created_at', 'updated_at',)
    list_per_page = 10


@admin.register(Feedback)
class FeedbackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Feedback Info', {
            'fields': ('name', 'message', 'rating',),
        }),

        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def rating_stars(self, obj):
        stars = '★' * obj.rating
        return format_html('<span style="color: orange;">{}</span>', stars)

    rating_stars.short_description = "Rating"

    def has_add_permission(self, request):
        return False

    list_display = ['name', 'message', 'rating_stars', ]
    list_filter = ('name', 'rating', 'created_at', 'updated_at',)
    search_fields = ('name', 'message', 'rating',)
    readonly_fields = ('name', 'message', 'rating', 'created_at', 'updated_at',)
    list_per_page = 10
