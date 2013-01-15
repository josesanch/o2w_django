from django import forms
from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.contrib.comments.forms import CommentForm
from models import CommentWithRatings
from django.utils.safestring import mark_safe

class RatingWidget(Widget):

    def render(self, name, value, attrs=None):
        real_attrs = self.attrs
        real_attrs['type'] = 'hidden';
        real_attrs['name'] = name
        real_attrs['value'] = value or 0

        stars = [u'<input%s />' % flatatt(real_attrs)]
        for i in range(1,6):
            stars.append("<img class='star' data-position='%s' id='rating-%s' src='/static/images/ui/star_off.gif'>" % (i, i))

        input = "<div class='rating-container'>" + "".join(stars) + "</div>"
        return mark_safe(input)

    def id_for_label(self, id_):
        return '%s_rating' % id_

    id_for_label = classmethod(id_for_label)
    class Media:
        js = ('js/rating.js',)


class CommentFormWithRatings(CommentForm):

    rating = forms.IntegerField()

    def __init__(self, target_object, data=None, initial=None):
        self.base_fields.insert(
            0,
            'title',
            forms.CharField(max_length=300)
        )
        self.base_fields.insert(
            1,
            'rating',
            forms.IntegerField(widget=RatingWidget)
        )
        self.base_fields.insert(
            2,
            'age',
            forms.CharField(max_length=50)
        )
        self.base_fields.insert(
            3,
            'location',
            forms.CharField(max_length=50)
        )

        super(CommentFormWithRatings, self).__init__(target_object=target_object, data=data, initial=initial)



    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentWithRatings

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormWithRatings, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        data['rating'] = self.cleaned_data['rating']
        data['age'] = self.cleaned_data['age']
        data['location'] = self.cleaned_data['location']
        return data
