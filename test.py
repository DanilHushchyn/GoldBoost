from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

print(urlsafe_base64_encode(force_bytes(4)))