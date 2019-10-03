from generic.helper import encode as token_encode

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


def verify_email(request, user):

	current_site = get_current_site(request)
	context = {
		'user' : user,
		'domain' : current_site.domain,
		'token' : token_encode({'user_id': user.id, 'email': user.email })
	}

	message = render_to_string('authentication/verify_email.html', context)
	mail = EmailMessage(subject='Email Verification', body=message, to=[user.email])
	mail.send()
