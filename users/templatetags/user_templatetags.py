from users.models import SocialIcon
from django import template
register = template.Library()

@register.simple_tag
def get_social_icon():
    #social_apps = SocialIcon.objects.all()
    social_apps = {str(social.name):str(social.image) for social in SocialIcon.objects.all()}
    return social_apps