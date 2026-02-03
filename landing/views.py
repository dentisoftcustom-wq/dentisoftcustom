from django.shortcuts import render
from .forms import LeadForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



def landing_page(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()

            # -----------------------------
            # 1️⃣ EMAIL PARA TI (ADMIN)
            # -----------------------------
            send_mail(
                subject='New Demo Request – Dentisoft Custom',
                message=f"""
                A new demo request has been submitted.

                Clinic: {lead.clinic_name}
                Contact Name: {lead.contact_name}
                Email: {lead.email}
                Phone: {lead.phone}

                Please contact this clinic to schedule the demo.
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['dentisoftcustom@gmail.com'],
                fail_silently=False,
            )

            # --------------------------------
            # EMAIL HTML PARA EL CLIENTE
            # --------------------------------
            subject = 'We received your Dentisoft Custom demo request'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [lead.email]

            text_content = f"""
            Hello {lead.contact_name},

            Thank you for contacting Dentisoft Custom.
            We have received your demo request and will contact you shortly.

            Dentisoft Custom Team
            """

            html_content = render_to_string(
                'emails/demo_confirmation.html',
                {'name': lead.contact_name}
            )

            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, "text/html")
            email.send()


            return render(request, 'landing/thank_you.html')

    else:
        form = LeadForm()

    return render(request, 'landing/landing.html', {'form': form})
