from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm
from .models import Photo, Mountain, Badge

@login_required
def upload_photo(request):
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

def calculate_badge_stats(badge, visited_ids):
    """Helper function to calculate stats for a single badge."""
    required_ids = set(badge.mountains.values_list('id', flat=True))
    total_required = len(required_ids)
    
    # Intersection logic stays the same but encapsulated
    visited_in_badge = required_ids.intersection(visited_ids)
    current_progress = len(visited_in_badge)
    
    return {
        'obj': badge,
        'is_unlocked': (current_progress == total_required) and (total_required > 0),
        'current': current_progress,
        'total': total_required,
        'percent': int((current_progress / total_required) * 100) if total_required > 0 else 0
    }

@login_required
def profile(request):
    user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # 1. Functional extraction of visited IDs
    visited_ids = set(user_photos.filter(matched_mountain__isnull=False)
                                 .values_list('matched_mountain__id', flat=True))
    
    visited_mountains = Mountain.objects.filter(id__in=visited_ids).distinct()
    all_mountains_count = Mountain.objects.count()

    # 2. Functional Badge Progress (List Comprehension)
    all_badges = Badge.objects.prefetch_related('mountains').all()
    
    # We map the calculate_badge_stats function over the badges collection
    badges_status = [calculate_badge_stats(badge, visited_ids) for badge in all_badges]

    context = {
        'photos': user_photos,
        'visited_mountains': visited_mountains,
        'progress': f"{len(visited_ids)} / {all_mountains_count}",
        'badges_status': badges_status,
    }
    return render(request, 'profile.html', context)