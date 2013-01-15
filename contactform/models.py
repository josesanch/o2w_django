from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from django.db import models

class ContactFormPluginModel(CMSPlugin):
    title = models.CharField(_("Title"), blank=True, max_length=100)
    email = models.EmailField(_("E-mail to send the data"), blank=True, max_length=180)
    subject = models.CharField(_("Subject"), blank=True, max_length=100)
    submit_button = models.CharField(_("Submit button"), blank=True, max_length=100, default=_('Submit'))
    thankyou_message = models.TextField(_('Thank you Message'))
    def __unicode__(self):
        return self.title


class ContactFormBase(models.Model):
    """
    Base class for contact form you can inherit from this in order to
    extend
    """
    name = models.CharField(_("Name"), max_length = 255)
    location = models.CharField(_("Location"), max_length = 255)
    phone = models.CharField(_("Contact phone"), max_length=20)
    email = models.EmailField(_("Contact e-mail"), max_length=80)
    message = models.TextField(_("Message"))
    form = models.ForeignKey(ContactFormPluginModel)

    class Meta:
        abstract = True


    def __unicode__(self):
        return self.name

class Submit(ContactFormBase):
    pass
