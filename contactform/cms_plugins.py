#encoding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from models import ContactFormPluginModel
from o2w.contactform.forms import ContactForm
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)
class ContactUsFormPlugin(CMSPluginBase):
    name = _("Contact Us Form")
    module = 'O2W'
    model = ContactFormPluginModel
    render_template = "o2w_contactform/form.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        request = context['request']

        if request.method == 'POST':
            form = ContactForm(request.POST, label_suffix="")
            if form.is_valid():
                # Aquí enviamos el correo.
                from django.core.mail import send_mail
                email_text = render_to_string('o2w_contactform/email.txt', {}, context)

                send_mail(
                    instance.subject,
                    email_text,
                    instance.email,
                    [instance.email]
                )


                submit = form.save(commit=False)
                submit.form = instance
                submit.save()
                form = None

        else:
            form = ContactForm(label_suffix="")

        context.update({'form': form, 'instance': instance })
        return context


plugin_pool.register_plugin(ContactUsFormPlugin)
