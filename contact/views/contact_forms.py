from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact


def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context = {
            'site_title': 'Create - ',
            'form': form,
            'form_action': form_action
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)

        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'site_title': 'Create - ',
        'form': ContactForm(),
        'form_action': form_action
    }

    return render(
        request,
        'contact/create.html',
        context,
    )


def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        context = {
            'site_title': 'Update - ',
            'form': form,
            'form_action': form_action
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'site_title': 'Update - ',
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }

    return render(
        request,
        'contact/create.html',
        context,
    )