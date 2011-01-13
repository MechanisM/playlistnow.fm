from django import forms
from django.template import defaultfilters
from django.contrib.auth.models import User

class PostRegistrationForm(forms.ModelForm):
    location = forms.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs.keys():
            kwargs['initial'] = {}
        
        request = kwargs.pop('request')
        
        instance = kwargs['instance']
        if getattr(request, 'facebook', False):
            upstream = request.facebook.graph.request(request.facebook.user['uid'])
            initial = {
                'first_name': upstream['first_name'],
                'last_name': upstream['last_name'],
                'location': upstream['location']['name'],
                'email': upstream['email'],
            }
            kwargs['initial'].update(initial)

        if instance.gfcprofile_set.count() >= 1:
            pass
        if instance.twitterprofile_set.count() >= 1:
            pass

        if instance.playlistprofile.user_location:
            kwargs['initial']['location'] = instance.playlistprofile.user_location

        super(PostRegistrationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.required = True

    def save(self, commit=True):
        self.instance.playlistprofile.user_location = self.cleaned_data['location']
        self.instance.playlistprofile.save()
        object = super(PostRegistrationForm, self).save(commit=commit)

        proposed_username = '%s %s' % (
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name']
        )
        proposed_username = defaultfilters.slugify(proposed_username)
        while User.objects.filter(username=proposed_username).count():
            if object in User.objects.filter(username=proposed_username):
                break
            proposed_username += '-'
        object.username = proposed_username
        object.save()
        return object

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
