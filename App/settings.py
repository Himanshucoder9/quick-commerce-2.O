import os
from pathlib import Path
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

DEFAULT_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_ckeditor_5',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'corsheaders',
    'import_export',
    # 'django_filters',
    # 'django.contrib.admindocs',
]

LOCAL_APPS = [
    'Auth',
    'General',
    'Master',
    'Customer',
    'Warehouse',
    'Delivery',
    # 'Product',
    # 'Vendor',
    # 'Notification',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'App.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'App.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': config('ENGINE'),
#         'NAME': config('NAME'),
#         'USER': 'root',
#         'PASSWORD': config('PASSWORD'),
#         'HOST': config('HOST'),
#         'PORT': config('PORT'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR / "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for custom user model
AUTH_USER_MODEL = 'Auth.User'

# TWILIO
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# Razorpay
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')

# Domain
TEMPLATES_BASE_URL = config('TEMPLATES_BASE_URL')

X_FRAME_OPTIONS = config('X_FRAME_OPTIONS')

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_USE_TLS = True
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

REST_FRAMEWORK = {
    # For Token Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # SPECTACULAR_SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# Cors Header
CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "https://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
    "http://localhost:3000",
    "http://localhost:5500",
    "https://www.m4bistro.in",
    "https://8bf4-2401-4900-8823-6c56-d52e-9588-97ae-d146.ngrok-free.app",
]

# Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Quick Commerce Admin",
    "site_header": "Quick Commerce Admin",
    "site_brand": "Quick Commerce Admin",
    "site_logo": "assets/img/q1.png",

    "login_logo": "assets/img/q1.png",
    "login_logo_dark": None,
    "site_logo_classes": None,

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    # "site_icon": "frontend/assets/img/favicon.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to Quick Commerce",

    # Copyright on the footer
    "copyright": "Quick Commerce",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "#", "new_window": True},

        {"name": "Vist Site", "url": "http://127.0.0.1:8000", "new_window": True},

    ],

    "usermenu_links": [
        {"model": "auth.user"}
    ],

    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["Auth", "Core",
                              "Auth.User", "Auth.CustomAdmin", "Auth.Customer", "Auth.VendorShop", "Auth.Agent",
                              "Core.SiteConfig", "Core.SocialMedia", "Core.Banner", "Core.About", "Core.PrivacyPolicy",
                              "Core.TermsAndCondition", "Core.FAQCategory", "Core.FAQ", "Core.Contact", "Core.Feedback",
                              "Product.Country", "Product.Tax",
                              "Product.Unit", "Product.Category", "Product.SubCategory", "Product.PackagingType",
                              "Product.Product", "Product.ShippingAddress", "Product.Cart", "Product.CartItem",
                              "Product.Order", "Product.OrderItem", "Product.Payment"
                              ],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "Core": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,
    # 5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,
    # 5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2 for the full
    # list of 5.13.0 free icon classes
    "icons": {
        # Auth
        "Auth.User": "fas fa-users-cog",
        "Auth.CustomAdmin": "fas fa-user-shield",
        "Auth.VendorShop": "fas fa-users",
        "Auth.Agent": "fas fa-user-shield",
        "Auth.Customer": "fas fa-user-friends",
        "Auth.Driver": "fas fa-user-tie",

        # Core
        "Core.SiteConfig": "fas fa-globe",
        "Core.SocialMedia": "fas fa-hashtag",
        "Core.About": "far fa-address-card",
        "Core.Banner": "fas fa-images",
        "Core.PrivacyPolicy": "fas fa-user-lock",
        "Core.TermsAndCondition": "fas fa-check",
        "Core.FAQCategory": "fas fa-layer-group",
        "Core.FAQ": "fas fa-question",
        "Core.Contact": "fas fa-comments",
        "Core.Feedback": "fas fa-star",

        #Delivery
        "Delivery.DeliveryAddress": "fas fa-biking",

        # Product
        "Product.Country": "fas fa-globe-africa",
        "Product.Tax": "fas fa-file-invoice-dollar",
        "Product.Unit": "fas fa-balance-scale-right",
        "Product.Category": "fas fa-shapes",
        "Product.SubCategory": "fas fa-layer-group",
        "Product.PackagingType": "fas fa-box-open",
        "Product.Product": "fas fa-people-carry",
        "Product.ShippingAddress": "fas fa-map-marker-alt",
        "Product.Cart": "fas fa-shopping-cart",
        "Product.CartItem": "fas fa-cart-plus",
        "Product.Order": "fas fa-shipping-fast",
        "Product.OrderItem": "fas fa-truck",
        "Product.Payment": "fas fa-rupee-sign",

        # Vendor
        "Vendor.BusinessCategory": "fas fa-briefcase",
        "Vendor.CategoryRequest": "fas fa-list",
        "Vendor.Support": "fas fa-headset",

        # Site
        "sites.site": "fas fa-globe",

    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-caret-right",
    "default_icon_children": "fas fa-caret-right",
    "related_modal_active": True,

    "custom_css": "assets/css/myadmin.css",
    "custom_js": "assets/js/myadmin.js",
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    "language_chooser": None,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-info",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": False,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# CKEDITOR_5_
customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

# CKEDITOR_5_
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload"
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
    },
}

# SPECTACULAR

SPECTACULAR_SETTINGS = {
    'TITLE': 'Quick Commerce API',
    'DESCRIPTION': 'Quick Commerce API documentation',
    'VERSION': '1.0.0.0 Beta',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Set session engine
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions
# SESSION_COOKIE_AGE = 3600  # 5 minutes in seconds
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_SECURE = False  # Set to True only if using HTTPS
# SESSION_COOKIE_HTTPONLY = True

# Notification
PUSH_NOTIFICATION_URL = 'https://fcm.googleapis.com/v1/projects/quickecommerce-a7b00/messages:send'
PUSH_NOTIFICATION_API_KEY = 'ya29.c.c0ASRK0GbnsfSX7wDkNyik0CqpUHIWd5oaHNM9UUP724kBbLqbdMZQrhtHzOrpEFowPzYX0lxvw4xrZ6EXA6d7QXbMFlYpcGU5W8f8aFFtwkpxDbNtd3tE0jtuCSnwVXJh8mW7nt8K9s5eJ22Pz3_CGFpEYghfDVPF3KxKjg6NU6_GgNwen1ZiKADTYVJaIfRIY7MR9gQKKJt1I2XucQp3HTaT6ntnPziuh7IUcHe3jkBRuFGfGp5M0Qcs4v3QyfXYdCvrscW0xh6cwks2X7EcSghmgSY2yQkzxHJ0h-fnNK53xBUSiCtRpbY2G1y8pLExTZY0Ua_Yc35FpV7LTA-Hhc2TlAkC56q2L0SXEVn7_jxGDnGJqmogyMylRewT388K5S8xcSnu5s3xIfeZqSoBU0_eXe6yVvxuzih5J01z6QzQr8fk1fojs7gflssgtUUrZop7bu8ZR01t9848mS5p2Xk6kZaSrbh9ph-bVBQuuggrbFl2VSdgiaZ83uJ8-xRJF-yray0m6elcz3ys_i1pOvuaW20bUivZrragcUB44nyr-p_n4fIblxYJt3nSQUyMMhspWjbJeatJJs0SWxrlRZmfvupUBrb53vaVi6eOFfwxor9dtsk4h7QpzUetfsQs4YnImd4MeZ_U_RrJM4vo-_RIwQIZs7I5z69au3JrI6-X49k2kUXRdOMOhaugx5n0ZxYUu4ViBk1-IIge7kIV-3FF9Z6er57Sh7eSoVMijU9fo6B3hWVRamoSORO-psSYIOz-7n3tw1MQ9fzp5hS0OoUyxbJqQVae40Ufh592yF8kqY4Y_wR4ImFmzRMB7MySR4d13gXe7beX4uv2XBqoQI6kxRhgvyYykQBm9rWb3x2iwwl-dpuWu2Mutkv72_2fIgQWS-1XSfx8e5mhIO8iBYZ5eaSbmeJxVnBaW79fBzhxy9I1k71eac1wQqsmpaMM7bI7IRu6Su7qRQ4q2iMMW_p45wIoaaaOM26gOrl'
# FCM_DJANGO_SETTINGS = {
#     "FCM_SERVER_KEY": "ya29.c.c0ASRK0GbnsfSX7wDkNyik0CqpUHIWd5oaHNM9UUP724kBbLqbdMZQrhtHzOrpEFowPzYX0lxvw4xrZ6EXA6d7QXbMFlYpcGU5W8f8aFFtwkpxDbNtd3tE0jtuCSnwVXJh8mW7nt8K9s5eJ22Pz3_CGFpEYghfDVPF3KxKjg6NU6_GgNwen1ZiKADTYVJaIfRIY7MR9gQKKJt1I2XucQp3HTaT6ntnPziuh7IUcHe3jkBRuFGfGp5M0Qcs4v3QyfXYdCvrscW0xh6cwks2X7EcSghmgSY2yQkzxHJ0h-fnNK53xBUSiCtRpbY2G1y8pLExTZY0Ua_Yc35FpV7LTA-Hhc2TlAkC56q2L0SXEVn7_jxGDnGJqmogyMylRewT388K5S8xcSnu5s3xIfeZqSoBU0_eXe6yVvxuzih5J01z6QzQr8fk1fojs7gflssgtUUrZop7bu8ZR01t9848mS5p2Xk6kZaSrbh9ph-bVBQuuggrbFl2VSdgiaZ83uJ8-xRJF-yray0m6elcz3ys_i1pOvuaW20bUivZrragcUB44nyr-p_n4fIblxYJt3nSQUyMMhspWjbJeatJJs0SWxrlRZmfvupUBrb53vaVi6eOFfwxor9dtsk4h7QpzUetfsQs4YnImd4MeZ_U_RrJM4vo-_RIwQIZs7I5z69au3JrI6-X49k2kUXRdOMOhaugx5n0ZxYUu4ViBk1-IIge7kIV-3FF9Z6er57Sh7eSoVMijU9fo6B3hWVRamoSORO-psSYIOz-7n3tw1MQ9fzp5hS0OoUyxbJqQVae40Ufh592yF8kqY4Y_wR4ImFmzRMB7MySR4d13gXe7beX4uv2XBqoQI6kxRhgvyYykQBm9rWb3x2iwwl-dpuWu2Mutkv72_2fIgQWS-1XSfx8e5mhIO8iBYZ5eaSbmeJxVnBaW79fBzhxy9I1k71eac1wQqsmpaMM7bI7IRu6Su7qRQ4q2iMMW_p45wIoaaaOM26gOrl"
# }
