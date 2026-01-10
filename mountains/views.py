from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm
from .models import Photo, Mountain, Badge

@login_required
def upload_photo(request):
    # (Same as before)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def profile(request):
    user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # 1. Get IDs of all unique mountains visited by the user
    visited_ids = set(user_photos.filter(matched_mountain__isnull=False).values_list('matched_mountain__id', flat=True))
    
    visited_mountains = Mountain.objects.filter(id__in=visited_ids).distinct()
    all_mountains_count = Mountain.objects.count()

    # 2. Calculate Badge Progress
    all_badges = Badge.objects.prefetch_related('mountains').all()
    badges_status = []

    for badge in all_badges:
        required_ids = set(badge.mountains.values_list('id', flat=True))
        total_required = len(required_ids)
        
        # Intersection: mountains required for this badge that the user HAS visited
        visited_in_badge = required_ids.intersection(visited_ids)
        current_progress = len(visited_in_badge)
        
        is_unlocked = (current_progress == total_required) and (total_required > 0)
        
        percent = int((current_progress / total_required) * 100) if total_required > 0 else 0

        badges_status.append({
            'obj': badge,
            'is_unlocked': is_unlocked,
            'current': current_progress,
            'total': total_required,
            'percent': percent
        })

    context = {
        'photos': user_photos,
        'visited_mountains': visited_mountains,
        'progress': f"{len(visited_ids)} / {all_mountains_count}",
        'badges_status': badges_status, # Pass the calculated list
    }
    return render(request, 'profile.html', context)