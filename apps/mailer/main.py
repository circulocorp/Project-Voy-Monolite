from django.template.loader import render_to_string
from django.core.mail import send_mail


class Mailer:

    def __init__(self, sender='notificaciones@circulocorp.com'):
        self.sender = sender

    def send_signup_email(self, email, password, otp, url):

        html_content = render_to_string('renders/signUp.html', {
            'otp': otp,
            'password': password,
            'url': url,
            'email': email,
        })

        try:
            send_mail(
                'Verificación cuenta Voy.',
                html_content,
                self.sender,
                [email],
                fail_silently=False,
                html_message=html_content
            )

            print('Email enviado a:', email)
        except Exception as e:
            print('Error al enviar el correo:', e)