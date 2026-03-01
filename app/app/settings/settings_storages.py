from decouple import config

R2_ACCOUNT_ID = config("R2_ACCOUNT_ID")
R2_BUCKET = config("R2_BUCKET")
R2_PUBLIC_DOMAIN = config("R2_PUBLIC_DOMAIN", default="")

R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

COMMON_R2_OPTIONS = {
    "endpoint_url": R2_ENDPOINT,
    "access_key": config("R2_ACCESS_KEY_ID"),
    "secret_key": config("R2_SECRET_ACCESS_KEY"),
    "region_name": "auto",
    "signature_version": "s3v4",
    "addressing_style": "virtual",
    "default_acl": None,
    "querystring_auth": False,
}

if R2_PUBLIC_DOMAIN:
    COMMON_R2_OPTIONS["custom_domain"] = R2_PUBLIC_DOMAIN
    COMMON_R2_OPTIONS["url_protocol"] = "https:"

STORAGES = {
    "default": {  # MEDIA
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **COMMON_R2_OPTIONS,
            "bucket_name": R2_BUCKET,
            "location": "media",
            "file_overwrite": False,
        },
    },
    "staticfiles": {  # STATIC
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **COMMON_R2_OPTIONS,
            "bucket_name": R2_BUCKET,
            "location": "static",
        },
    },
}
