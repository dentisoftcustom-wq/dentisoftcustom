
# Create your views here.
from django.shortcuts import render, redirect
from .forms import LeadForm

def landing_page(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'landing/thank_you.html')
    else:
        form = LeadForm()
    return render(request, 'landing/landing.html', {'form': form})

