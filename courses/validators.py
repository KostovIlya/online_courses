import re

from rest_framework.exceptions import ValidationError


class DescriptionUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        domain_pattern = r'(?<!@)\b(\w[\w.-]+\.\w+)\b'
        youtube_url_pattern = r'(?:https?://)?(?:www\.)?youtube.com'
        field = value.get(self.field)

        try:
            all_links = re.findall(domain_pattern, field)
        except TypeError:
            all_links = None

        if all_links:
            for link in all_links:
                if not bool(re.match(youtube_url_pattern, link)):
                    raise ValidationError('Недопустимый URL!')
