from django import http
from django import shortcuts
from django import template
from django.core import urlresolvers
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from socialregistration.views import _get_next

from models import GfcProfile

if not hasattr(settings, 'GOOGLE_SITE_ID'):
    raise Exception('Please set GOOGLE_SITE_ID in settings.py')

def gfc_callback(request,
    template_name='gfc/callback.html', extra_context=None):
    context = {}
    context.update(extra_context or {})

    uid = request.COOKIES.get('fcauth' + settings.GOOGLE_SITE_ID, False)
    if uid is None:
        context.error = GFC_ERROR
        return shortcuts.render_to_response(template_name, context,
            context_instance=template.RequestContext(request))

    user = auth.authenticate(uid=uid)

    if user is None:
        request.session['socialregistration_user'] = User()
        request.session['socialregistration_profile'] = GfcProfile(uid=uid)
        request.session['next'] = _get_next(request)
        return http.HttpResponseRedirect(urlresolvers.reverse('socialregistration_setup'))

    if not user.is_active:
        return shortcuts.render_to_response(account_inactive_template, context,
            context_instance=RequestContext(request))

    auth.login(request, user)

    return http.HttpResponseRedirect(_get_next(request))

    context.update(extra_context or {})
    return shortcuts.render_to_response(template_name, context,
        context_instance=template.RequestContext(request))

def gfc_redirect(request,
    template_name='gfc/redirect.html', extra_context=None):

    context = {
        'gfc_site_id': settings.GOOGLE_SITE_ID,
    }

    context.update(extra_context or {})
    return shortcuts.render_to_response(template_name, context,
        context_instance=template.RequestContext(request))