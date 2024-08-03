import uuid
from django.utils.text import slugify
from functools import partial


def image_rename(instance, filename, path):
    extension = filename.split('.')[-1]
    new_filename = f"{slugify(instance.title)}-{uuid.uuid4()}.{extension}"
    return f"{path}/{new_filename}"


def image_with_path(path):
    return partial(image_rename, path=path)
