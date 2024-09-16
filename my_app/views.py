from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from .forms import ContactForm

def contact_message(request):
    form = ContactForm()
    message_time = request.session.get('message_time', None)

    if message_time:
        message_time = timezone.datetime.fromisoformat(message_time)
        if (timezone.now() - message_time).total_seconds() < 600:
            if request.method == 'GET':
                # Xatolik bo'lsa, `message_display` sahifasini render qilish
                return render(request, 'my_app/message_display.html', {
                    'status': 'error',
                    'message': "Siz habar yuborgansiz 10 daqiqadan keyin urinib ko'ring"
                })

            return JsonResponse({
                'status': 'error',
                'message': "Siz habar yuborgansiz 10 daqiqadan keyin urinib ko'ring"
            })

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['message_time'] = timezone.now().isoformat()
            return JsonResponse({
                'status': 'success',
                'message': 'Xabaringiz yuborildi'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Forma to\'ldirilmagan yoki noto\'g\'ri'
            })

    return render(request, 'my_app/contact_form.html', {'form': form})
