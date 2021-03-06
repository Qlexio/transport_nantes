from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
# from django.urls import reverse
# from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from .forms import MailingListSignupForm, QuickMailingListSignupForm
from .models import MailingList, MailingListEvent

# Create your views here.

class MailingListSignup(FormView):
    template_name = 'mailing_list/signup.html'
    merci_template = 'mailing_list/merci.html'
    form_class = MailingListSignupForm
    # success_url = reverse_lazy('mailing_list:list_ok')

    # We don't currently populate this form with the user's current
    # subscriptions.  If the user is logged in, we should.  This then
    # becomes the edit form as well.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = 'asso_tn/images-libres/black-and-white-bridge-children-194009-1000.jpg'
        context['hero_title'] = 'Newsletter'
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        subscribe = False
        user = form.save(commit=False)
        try:
            user.refresh_from_db()
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            pass            # I'm not sure this can ever happen.
        if user is None or user.pk is None:
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user is None:
                user = User()   # New user.
                user.username = get_random_string(20)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
        user.save()
        user.profile.commune = form.cleaned_data['commune']
        user.profile.code_postal = form.cleaned_data['code_postal']
        user.profile.save()
        for newsletter in form.cleaned_data['newsletters']:
            subscription = MailingListEvent.objects.create(
                user=user,
                mailing_list=newsletter,
                event_type=MailingListEvent.EventType.SUBSCRIBE)
            subscription.save()
            # At some point we should also store the last known
            # subscription state in a table with foreign key user.  If
            # the user is in that table, we use it, otherwise we look
            # up in mailing_list_events.  (We'll always need this
            # extra lookup, because a newly created list won't
            # populate users' current (unsubscribed) state.
            #
            # We should wait until this is a performance issue, however.
            subscribe = True
        if subscribe:
            return render(
                self.request, self.merci_template,
                {
                    'hero': True,
                    'hero_image':
                    'asso_tn/images-libres/black-and-white-bridge-children-194009-1000.jpg',
                    'hero_title': 'Newsletter',
                }
            )
        return super(MailingListSignup, self).form_valid(form)

class QuickMailingListSignup(FormView):
    template_name = 'mailing_list/quick_signup.html'
    merci_template = 'mailing_list/merci.html'
    form_class = MailingListSignupForm

    # We don't currently populate this form with the user's current
    # subscriptions.  If the user is logged in, we should.  This then
    # becomes the edit form as well.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = 'asso_tn/images-libres/black-and-white-bridge-children-194009-1000.jpg'
        context['hero_title'] = 'Newsletter'
        return context

    def form_invalid(self, form):
        """Display the correct form.

        This is actually a bit of a hack.  We should build the correct
        form, extract the email address from the incoming form, and
        then display the correct thing.  I think.

        This should also pre-select one newsletter, which should be a
        change to the newsletter model.  If the user is logged in, it
        should also pre-populate the subscribed newsletters.

        """
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        """Process a valid MailingListSignupForm.

        This method is called when valid form data has been POSTed.
        It returns an HttpResponse.
        """
        subscribe = False
        user = form.save(commit=False)
        try:
            user.refresh_from_db()
        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            pass            # I'm not sure this can ever happen.
        if user is None or user.pk is None:
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user is None:
                user = User()   # New user.
                user.username = get_random_string(20)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
        user.save()
        user.profile.commune = form.cleaned_data['commune']
        user.profile.code_postal = form.cleaned_data['code_postal']
        user.profile.save()
        for newsletter in form.cleaned_data['newsletters']:
            subscription = MailingListEvent.objects.create(
                user=user,
                mailing_list=newsletter,
                event_type=MailingListEvent.EventType.SUBSCRIBE)
            subscription.save()
            # At some point we should also store the last known
            # subscription state in a table with foreign key user.  If
            # the user is in that table, we use it, otherwise we look
            # up in mailing_list_events.  (We'll always need this
            # extra lookup, because a newly created list won't
            # populate users' current (unsubscribed) state.
            #
            # We should wait until this is a performance issue, however.
            subscribe = True
        if subscribe:
            return render(
                self.request, self.merci_template,
                {
                    'hero': True,
                    'hero_image':
                    'asso_tn/images-libres/black-and-white-bridge-children-194009-1000.jpg',
                    'hero_title': 'Newsletter',
                }
            )
        return super(MailingListSignup, self).form_valid(form)

class MailingListMerci(TemplateView):
    """View class only used whilst debugging.

    This is useful for revealing the thank you page, but under normal
    circumstances it should not be revealed without first filling out
    the form.

    """
    template_name = 'mailing_list/merci.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = True
        context['hero_image'] = 'asso_tn/images-libres/black-and-white-bridge-children-194009-1000.jpg'
        context['hero_title'] = 'Newsletter'
        context['hero_description'] = '(actuellement debugging)'
        return context

