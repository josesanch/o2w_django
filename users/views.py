#from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.views import logout as logout_v, login as login_v
from forms import UserForm
from django.contrib.auth import authenticate, login as login_auth
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
def login(request):
    return login_v(request)

def logout(request):
    return logout_v(request, reverse('user-login'))


class SignupView(generic.TemplateView):
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        data = None
        if self.request.method == 'POST':
            data = self.request.POST

        form = UserForm(data)
        context['object'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = context['object']
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.save()

            auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login_auth(request, auth)
            return redirect(settings.LOGIN_REDIRECT_URL)

        return self.render_to_response(context)
