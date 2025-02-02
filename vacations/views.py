from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vacation, VacationEvent
from .forms import VacationForm, AddEventToVacationForm
from django.views.decorators.http import require_POST

@login_required
def dashboard(request):
    vacations = Vacation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'vacations/dashboard.html', {'vacations': vacations})

@login_required
def create_vacation(request):
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.user = request.user
            vacation.save()
            return redirect('vacations:dashboard')
    else:
        form = VacationForm()
    return render(request, 'vacations/create_vacation.html', {'form': form})

@login_required
@require_POST
def add_event_to_vacation(request):
    form = AddEventToVacationForm(request.POST, user=request.user)
    if form.is_valid():
        vacation = form.cleaned_data['vacation']
        # Gather event data from POST; adjust keys as necessary
        event_data = {
            'event_id': request.POST.get('event_id', ''),
            'name': request.POST.get('name', ''),
            'date': request.POST.get('date', None),
            'venue': request.POST.get('venue', ''),
            'description': request.POST.get('description', ''),
            'image_url': request.POST.get('image_url', ''),
            'event_url': request.POST.get('event_url', ''),
        }
        new_event = VacationEvent.objects.create(vacation=vacation, **event_data)
        # Return a JSON response with success message and maybe the new event details
        response_data = {
            'success': True,
            'message': f"Event '{new_event.name}' added to vacation '{vacation.name}'.",
            'event': {
                'id': new_event.id,
                'name': new_event.name,
                'date': new_event.date,
                'venue': new_event.venue,
            }
        }
        return JsonResponse(response_data)
    else:
        # Return error messages
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
def save_event_to_vacation(request):
    if request.method == "POST":
        vacation_id = request.POST.get("vacation_id")
        vacation = get_object_or_404(Vacation, id=vacation_id, user=request.user)

        event_id = request.POST.get("event_id")

        # Prevent duplicates
        if VacationEvent.objects.filter(vacation=vacation, event_id=event_id).exists():
            return JsonResponse({"success": False, "message": "Event already saved to this vacation."})

        VacationEvent.objects.create(
            vacation=vacation,
            event_id=event_id,
            name=request.POST.get("event_name", ""),
            date=request.POST.get("event_date", None),
            venue=request.POST.get("event_venue", ""),
            description=request.POST.get("event_description", ""),
            image_url=request.POST.get("event_image", ""),
            event_url=request.POST.get("event_url", "")
        )
        
        return JsonResponse({"success": True, "message": "Event saved successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request."})       