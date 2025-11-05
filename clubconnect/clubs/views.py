from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Club, Event, Membership, Message, Announcement
from accounts.models import User
from .forms import ClubForm, EventForm, ClubRegistrationForm, MessageForm, AnnouncementForm

@login_required
def clubs_list(request):
    clubs = Club.objects.all()
    return render(request, 'clubs/clubs_list.html', {'clubs': clubs})

# Admin-only club creation
@login_required
def create_club(request):
    if not request.user.is_admin():
        messages.error(request, "Only administrators can create clubs.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save()
            messages.success(request, f"Club '{club.name}' has been created successfully.")
            return redirect('assign_founder', club_id=club.id)
    else:
        form = ClubForm()
    
    return render(request, 'clubs/create_club.html', {'form': form})

# Admin assigns founder to club
@login_required
def assign_founder(request, club_id):
    if not request.user.is_admin():
        messages.error(request, "Only administrators can assign founders.")
        return redirect('dashboard')
    
    club = get_object_or_404(Club, id=club_id)
    query = request.GET.get('q', '').strip()
    # Default list shows existing founders; when searching, include students matching query
    base_qs = User.objects.filter(user_type='founder')
    if query:
        search_qs = User.objects.filter(user_type__in=['founder', 'student']).filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        potential_founders = search_qs.order_by('username')
    else:
        potential_founders = base_qs.order_by('username')
    
    if request.method == 'POST':
        founder_id = request.POST.get('founder_id')
        if founder_id:
            user_obj = get_object_or_404(User, id=founder_id)
            # Promote student to founder if needed
            if user_obj.user_type == 'student':
                user_obj.user_type = 'founder'
                user_obj.save()
                messages.info(request, f"{user_obj.username} was promoted to Founder.")
            # Assign as founder for the club
            club.founders.add(user_obj)
            messages.success(request, f"{user_obj.username} has been assigned as a founder of {club.name}.")
            return redirect('club_detail', club_id=club.id)
    
    return render(request, 'clubs/assign_founder.html', {
        'club': club,
        'potential_founders': potential_founders,
        'query': query,
    })

# Club detail view
def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    events = Event.objects.filter(club=club).order_by('start_time')
    founders = club.founders.all()
    announcements = Announcement.objects.filter(club=club).order_by('-created_at')[:5]
    is_member = False
    
    if request.user.is_authenticated:
        is_member = Membership.objects.filter(user=request.user, club=club, status='approved').exists()
    
    context = {
        'club': club,
        'events': events,
        'founders': founders,
        'announcements': announcements,
        'is_member': is_member,
    }
    return render(request, 'clubs/club_detail.html', context)

# Search clubs
def search_clubs(request):
    query = request.GET.get('q', '')
    clubs = Club.objects.all()
    
    if query:
        clubs = clubs.filter(
            Q(name__icontains=query) | 
            Q(short_description__icontains=query) |
            Q(domain_tags__icontains=query)
        )
    
    context = {
        'clubs': clubs,
        'query': query,
    }
    return render(request, 'clubs/search_results.html', context)

# Club registration for students
@login_required
def register_for_club(request, club_id):
    if not request.user.is_student():
        messages.error(request, "Only students can register for clubs.")
        return redirect('club_detail', club_id=club_id)
    
    club = get_object_or_404(Club, id=club_id)
    
    # Check if already a member or has pending request
    existing_membership = Membership.objects.filter(user=request.user, club=club).first()
    if existing_membership:
        if existing_membership.status == 'approved':
            messages.info(request, "You are already a member of this club.")
        elif existing_membership.status == 'pending':
            messages.info(request, "Your membership request is pending approval.")
        else:
            messages.info(request, "Your previous membership request was rejected.")
        return redirect('club_detail', club_id=club_id)
    
    if request.method == 'POST':
        form = ClubRegistrationForm(request.POST)
        if form.is_valid():
            membership = Membership(
                user=request.user,
                club=club,
                status='pending'
            )
            membership.save()
            messages.success(request, f"Your registration request for {club.name} has been submitted.")
            return redirect('dashboard')
    else:
        form = ClubRegistrationForm()
    
    return render(request, 'clubs/register_for_club.html', {'form': form, 'club': club})

# Direct messaging between students and founders
@login_required
def send_message_to_founder(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    founders = club.founders.all()
    
    if request.method == 'POST':
        founder_id = request.POST.get('founder_id')
        content = request.POST.get('content')
        
        if founder_id and content:
            founder = get_object_or_404(User, id=founder_id)
            message = Message(
                sender=request.user,
                receiver=founder,
                content=content,
                is_read=False
            )
            message.save()
            messages.success(request, "Your message has been sent to the club founder.")
            return redirect('club_detail', club_id=club_id)
    
    return render(request, 'clubs/send_message.html', {'club': club, 'founders': founders})

@login_required
def edit_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    # Check if user is a founder of this club
    if not club.founders.filter(id=request.user.id).exists():
        messages.error(request, "Only club founders can edit club information.")
        return redirect('club_detail', club_id=club_id)
    
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, f"Club '{club.name}' has been updated successfully.")
            return redirect('club_detail', club_id=club_id)
    else:
        form = ClubForm(instance=club)
    
    return render(request, 'clubs/edit_club.html', {'form': form, 'club': club})
@login_required
def create_event(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.founders.filter(id=request.user.id).exists():
        messages.error(request, "Only club founders can create events.")
        return redirect('club_detail', club_id=club_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, f"Event '{event.title}' has been created successfully.")
            return redirect('club_detail', club_id=club_id)
    else:
        form = EventForm()
    return render(request, 'clubs/create_event.html', {'form': form, 'club': club})

# Club member chat for members
@login_required
def club_chat(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    # Check if user is a founder or member of this club
    is_founder = club.founders.filter(id=request.user.id).exists()
    is_member = Membership.objects.filter(user=request.user, club=club, status='approved').exists()
    
    if not (is_founder or is_member):
        messages.error(request, "You must be a founder or member to access the club chat.")
        return redirect('club_detail', club_id=club.id)
    
    # Get all approved members
    members = Membership.objects.filter(club=club, status='approved')

    # Build recipient list: founders (for students) or members/admins (for founders)
    if is_founder:
        recipient_users = User.objects.filter(id__in=members.values_list('user_id', flat=True)) | User.objects.filter(user_type='admin')
    else:
        recipient_users = club.founders.all()
    recipient_users = recipient_users.distinct().order_by('username')

    # Handle sending a message
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        if receiver_id and content:
            receiver = get_object_or_404(User, id=receiver_id)
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                club=club,
                content=content.strip(),
                is_read=False,
            )
            messages.success(request, 'Message sent.')
            return redirect('club_chat', club_id=club_id)
        messages.error(request, 'Please select a recipient and enter a message.')

    # Load club-specific messages (between founders and members only)
    messages_qs = Message.objects.filter(club=club).order_by('created_at')
    
    context = {
        'club': club,
        'members': members,
        'is_founder': is_founder,
        'recipient_users': recipient_users,
        'messages': messages_qs,
    }
    return render(request, 'clubs/club_chat.html', context)

@login_required
def approve_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    club = membership.club

    # Ensure the user is a founder of the club
    if not club.founders.filter(id=request.user.id).exists():
        messages.error(request, "Only club founders can approve memberships.")
        return redirect('club_detail', club_id=club.id)

    membership.status = 'approved'
    membership.save()
    messages.success(request, f"Membership for {membership.user.username} has been approved.")
    return redirect('founder_dashboard')

@login_required
def leave_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    membership = get_object_or_404(Membership, user=request.user, club=club)

    if request.method == 'POST':
        membership.delete()
        messages.success(request, f"You have left {club.name}.")
        return redirect('club_detail', club_id=club.id)

    return render(request, 'clubs/leave_club_confirm.html', {'club': club})

@login_required
def reject_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    club = membership.club

    # Ensure the user is a founder of the club
    if not club.founders.filter(id=request.user.id).exists():
        messages.error(request, "Only club founders can reject memberships.")
        return redirect('club_detail', club_id=club.id)

    membership.status = 'rejected'
    membership.save()
    messages.success(request, f"Membership for {membership.user.username} has been rejected.")
    return redirect('founder_dashboard')

@login_required
def create_club_announcement(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.founders.filter(id=request.user.id).exists() and not request.user.is_staff:
        messages.error(request, "You are not authorized to create an announcement for this club.")
        return redirect('club_detail', club_id=club.id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = club
            announcement.save()
            messages.success(request, "Announcement created successfully.")
            return redirect('club_detail', club_id=club.id)
    else:
        form = AnnouncementForm()

    return render(request, 'clubs/create_club_announcement.html', {'form': form, 'club': club})

@login_required
def delete_club_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    club = announcement.club
    if not club.founders.filter(id=request.user.id).exists() and not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this announcement.")
        return redirect('club_detail', club_id=club.id)

    announcement.delete()
    messages.success(request, "Announcement deleted successfully.")
    return redirect('club_detail', club_id=club.id)
