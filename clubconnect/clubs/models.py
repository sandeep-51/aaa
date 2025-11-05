from django.db import models
from django.conf import settings

class Club(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    domain_tags = models.CharField(max_length=200, help_text="Comma separated tags")
    founders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='founded_clubs')
    faculty_advisor = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='event_qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_qr_code_url(self):
        from django.urls import reverse
        return reverse('event_checkin', kwargs={'event_id': self.id})

class Membership(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'club')
    
    def __str__(self):
        return f"{self.user.username} - {self.club.name}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('membership', 'Membership'),
        ('message', 'Message'),
        ('general', 'General'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ClubPost(models.Model):
    POST_TYPES = (
        ('event', 'Event'),
        ('info', 'Information'),
        ('meme', 'Meme'),
        ('general', 'General'),
    )
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='club_posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"
    
    def total_likes(self):
        return self.likes.count()

class MemberPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_points')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='member_points')
    points = models.IntegerField(default=0)
    participation_count = models.IntegerField(default=0)
    contribution_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'club')
        ordering = ['-points']
    
    def __str__(self):
        return f"{self.user.username} - {self.club.name}: {self.points} pts"

class Survey(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='surveys')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class SurveyQuestion(models.Model):
    QUESTION_TYPES = (
        ('text', 'Text'),
        ('choice', 'Multiple Choice'),
        ('rating', 'Rating (1-5)'),
    )
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    choices = models.TextField(blank=True, help_text="Comma separated choices for multiple choice")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.question_text

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('survey', 'user', 'question')
    
    def __str__(self):
        return f"{self.user.username} - {self.survey.title}"

class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    checked_in_at = models.DateTimeField(auto_now_add=True)
    checked_in_via_qr = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('event', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
