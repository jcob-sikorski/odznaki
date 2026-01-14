# mountains/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm
from .models import Photo, Mountain, Badge

@login_required
def upload_photo(request):
    """
    Handles the photo upload process.
    """
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False creates the object in memory but doesn't send to DB yet
            photo = form.save(commit=False)
            # Associate the photo with the currently logged-in user
            photo.user = request.user
            # Final save triggers the Database INSERT
            photo.save()
            return redirect('profile')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload.html', {'form': form})

def calculate_badge_stats(badge, visited_ids):
    """
    Pure helper function to calculate progress for a specific badge.
    Input: A Badge object, and a Set of mountain IDs the user has visited.
    """
    # Get IDs of all mountains required for this badge
    required_ids = set(badge.mountains.values_list('id', flat=True))
    total_required = len(required_ids)
    
    # Calculate intersection: Mountains required AND visited
    visited_in_badge = required_ids.intersection(visited_ids)
    current_progress = len(visited_in_badge)
    
    return {
        'obj': badge,
        # Badge is unlocked if progress equals requirement (and requirement isn't empty)
        'is_unlocked': (current_progress == total_required) and (total_required > 0),
        'current': current_progress,
        'total': total_required,
        'percent': int((current_progress / total_required) * 100) if total_required > 0 else 0
    }

@login_required
def profile(request):
    """
    User profile view. 
    Aggregates photo history and calculates badge progress using Set operations.
    """
    user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # 1. Functional extraction of visited IDs
    # We create a Set of IDs to make subsequent lookups O(1) instead of O(N)
    visited_ids = set(user_photos.filter(matched_mountain__isnull=False)
                                 .values_list('matched_mountain__id', flat=True))
    
    # Retrieve actual mountain objects for the list view
    visited_mountains = Mountain.objects.filter(id__in=visited_ids).distinct()
    all_mountains_count = Mountain.objects.count()

    # 2. Functional Badge Progress
    # prefetch_related reduces database queries (solving the N+1 problem)
    all_badges = Badge.objects.prefetch_related('mountains').all()
    
    # List comprehension maps the calculation function over all badges
    badges_status = [calculate_badge_stats(badge, visited_ids) for badge in all_badges]

    context = {
        'photos': user_photos,
        'visited_mountains': visited_mountains,
        'progress': f"{len(visited_ids)} / {all_mountains_count}",
        'badges_status': badges_status,
    }
    return render(request, 'profile.html', context)