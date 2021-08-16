from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class EmailAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        activate_url = context.get('activate_url')
        if activate_url:
            context['activate_url'] = f'{settings.FRONTEND_URL}/confirm-email/{context["key"]}'
        else:
            uid, token = context['password_reset_url'].split('/')[-2:]
            context['password_reset_url'] = f'{settings.FRONTEND_URL}/password-reset/{uid}/{token}'
        msg = self.render_mail(template_prefix, email, context)
        msg.send()


