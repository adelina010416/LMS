from rest_framework import serializers


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_link = 'youtube.com'
        if value.get(self.field):
            if youtube_link not in dict(value).get(self.field):
                raise serializers.ValidationError("You can only attach links to videos on YouTube.")
