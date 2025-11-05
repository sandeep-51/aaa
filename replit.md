# ClubConnect - College Club Management Platform

## Overview
ClubConnect is a comprehensive Django-based platform for managing college clubs, events, and student engagement. The platform supports admins, club founders, and students with role-based features.

## Project Structure
- **Django 5.2.7** with Python 3.11
- **Database**: SQLite3 (development), PostgreSQL compatible for production
- **Frontend**: Django templates with Bootstrap
- **Real-time Features**: WebSocket support available for live features

## Recent Changes (November 5, 2025)

### Bug Fixes and UI Improvements (Latest Session)

#### Fixed Notification System
- Updated notifications template to display **real notifications** from database instead of hardcoded mock data
- Created `dashboard/context_processors.py` to make unread notification count globally available
- Updated base template to show **actual unread notification count** instead of hardcoded "3"
- Notifications now properly highlight unread items with blue background
- Added auto-redirect to linked content when clicking notifications

#### Enhanced Club Detail Page
- Added **Recent Posts** section showing club member posts with images and likes
- Added **Active Surveys** section for ongoing club surveys
- Added **QR Code display** for events on club detail page
- Posts show author, post type, timestamp, and like count
- Survey section includes direct links for members and results view for founders

#### All Features Now Visible and Functional
All features mentioned in the testing guide are now properly implemented:
- ⭐ Add to Favorites
- 🏆 Leaderboard
- ✏️ Edit Club (founders)
- 📢 Create Announcement (founders)
- 📅 Create Event with QR Code (founders)
- 📊 Create Survey (founders)
- 🎥 Create Meeting (founders)
- 💬 View Feedbacks (founders)
- 👨‍🏫 Mentor Sessions (founders)
- 💬 Club Chat (members)
- ➕ Create Post (members)
- 💡 Submit Feedback (members)
- 👨‍🏫 Book Mentor Session (members)
- 🚪 Leave Club (members)

## Previous Changes (November 5, 2025)

### Initial Setup
- Configured Django for Replit environment (ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
- Set up database migrations and created initial schema
- Configured workflow to run on port 5000

### Core Features Implemented

#### 1. Active Status Optimization
- Updated `UpdateLastSeenMiddleware` with caching (30-second intervals)
- Reduced database writes while maintaining accurate status tracking
- Users marked online if active within last 5 minutes

#### 2. Admin Features
- User creation already existed, confirmed working
- Real-time dashboard analytics with API endpoint (`/dashboard/ajax/admin_analytics/`)
- Shows: signins, signups, total users, clubs, events (auto-refresh every 5 minutes)
- Club creation functionality available in manage clubs section

#### 3. Notification System
- Created `Notification` model with types: announcement, event, membership, message, general
- API endpoints for marking read and checking unread count
- Automatic notifications for:
  - New announcements (all users or club members)
  - New events (favorited users + club members)
  - Membership status changes
  - Feedback submissions
  - Mentor session requests

#### 4. Announcement Management
- Delete functionality with proper permissions (admin/founder only)
- Announcements now track author
- Notifications sent to relevant users on creation

#### 5. Activity Feed
- Scrollable feed at `/dashboard/activity-feed/`
- Shows recent announcements, upcoming events, and club posts
- Sorted by recency, limited to 20 items

#### 6. Social Media Features for Clubs
- `ClubPost` model with types: event, info, meme, general
- Image upload support
- Like system with many-to-many relationships
- Posts automatically notify club members
- Points awarded for posting (3 points + contribution count)

#### 7. Survey & Form System
- `Survey` and `SurveyQuestion` models
- Question types: text, multiple choice, rating (1-5)
- `SurveyResponse` for collecting answers
- Results visualization with:
  - Choice questions: count per option
  - Rating questions: average + distribution
  - Text questions: list of responses
- Points awarded for completing surveys (5 points)

#### 8. Member Ranking System
- `MemberPoints` model tracking:
  - Total points
  - Participation count (event attendance)
  - Contribution count (posts, surveys)
- Leaderboard view per club
- Points awarded for:
  - Event check-in: 10 points
  - Survey completion: 5 points
  - Creating posts: 3 points

#### 9. QR Code & Attendance Tracking
- `EventAttendance` model
- QR code generation using `qrcode` library
- QR codes use `reverse()` for proper URL routing
- Dynamic base URL from request or environment
- Attendance tracking linked to user accounts
- Automatic points on check-in

#### 10. Favorite Clubs
- Many-to-many `favorited_by` field on Club model
- Toggle favorite functionality
- Event notifications sent to users who favorited the club
- AJAX-enabled for smooth UX

#### 11. Feedback & Event Ideas System
- `ClubFeedback` model with types: feedback, event_idea, suggestion
- Status tracking: pending, reviewed, implemented
- Students can submit to any club
- Representatives notified on submission
- Status updates notify the submitter

#### 12. Mentoring System
- `MentorSession` model for booking mentor meetings
- Students (club members) can request sessions with preferred date/time
- Notifications sent to club representatives:
  - Founders
  - President
  - Vice President
- Representatives can approve/reject with meeting links
- Status tracking: pending, approved, rejected, completed

#### 13. Club Representative Roles
- Added `president` and `vice_president` fields to Club model
- `get_representatives()` method returns all (founders + president + VP)
- Used for permission checks and notifications

#### 14. Club Meeting System
- `ClubMeeting` model for audio/video meetings
- Created by club representatives
- Unique meeting links generated
- Participant tracking
- Meeting room interface ready for WebRTC integration
- Notifications sent to all club members

## Models Summary

### clubs.Club
- Basic info, logo, founders
- President, Vice President roles
- Favorited by (many-to-many)

### clubs.Event
- Title, description, location, dates
- QR code field
- Linked to club

### clubs.Announcement
- Title, content, author
- Linked to club or general

### clubs.Notification
- User-specific notifications
- Type, title, message, link
- Read status

### clubs.ClubPost
- Social media-style posts
- Post type, image, likes

### clubs.MemberPoints
- Points, participation, contributions
- Per user per club

### clubs.Survey, SurveyQuestion, SurveyResponse
- Complete survey system
- Multiple question types

### clubs.EventAttendance
- QR code check-ins
- Event participation tracking

### clubs.ClubFeedback
- Feedback and ideas from students
- Status workflow

### clubs.MentorSession
- Mentoring requests
- Representative assignment

### clubs.ClubMeeting
- Online meetings
- Participant tracking

## API Endpoints

### Dashboard
- `/dashboard/ajax/admin_analytics/` - Real-time analytics data
- `/dashboard/ajax/unread_notifications_count/` - Notification count
- `/dashboard/notifications/mark-read/<id>/` - Mark notification as read
- `/dashboard/activity-feed/` - Activity feed view

### Clubs
- `/clubs/<id>/toggle-favorite/` - Favorite/unfavorite club
- `/clubs/<id>/submit-feedback/` - Submit feedback
- `/clubs/<id>/feedback/` - View club feedbacks (representatives only)
- `/clubs/feedback/<id>/update/` - Update feedback status
- `/clubs/<id>/book-mentor/` - Book mentor session
- `/clubs/<id>/mentor-sessions/` - View sessions (representatives)
- `/clubs/mentor-session/<id>/update/` - Update session status
- `/clubs/<id>/create-meeting/` - Create club meeting
- `/clubs/<id>/meeting/<link>/` - Join meeting room
- `/clubs/<id>/create-survey/` - Create survey
- `/clubs/survey/<id>/` - Take survey
- `/clubs/survey/<id>/results/` - View results (founders)
- `/clubs/<id>/create-post/` - Create post
- `/clubs/post/<id>/like/` - Like/unlike post
- `/clubs/<id>/leaderboard/` - View member rankings
- `/clubs/event/<id>/generate-qr/` - Generate QR code
- `/clubs/event/<id>/checkin/` - Check in to event

## Dependencies
```
Django==5.2.7
Pillow==11.0.0
qrcode[pil]==8.0
django-crispy-forms==2.3
```

## Configuration
- **Port**: 5000 (frontend)
- **ALLOWED_HOSTS**: ['*']
- **CSRF_TRUSTED_ORIGINS**: ['https://*.replit.dev', 'https://*.repl.co']
- **AUTH_USER_MODEL**: 'accounts.User'

## Next Steps / Future Enhancements
1. **Video/Audio Integration**: Integrate Twilio or WebRTC for actual video calls in meeting rooms
2. **Email Notifications**: Send email notifications for important events
3. **Mobile App**: React Native or Flutter mobile application
4. **Advanced Analytics**: More detailed charts and insights
5. **File Sharing**: Document repository for clubs
6. **Calendar Integration**: Sync events with Google Calendar
7. **Push Notifications**: Browser push notifications for real-time updates

## Notes
- All sensitive data should use environment variables in production
- Replace SQLite with PostgreSQL for production
- Set DEBUG=False and configure STATIC_ROOT for production
- Implement rate limiting for API endpoints
- Add comprehensive test coverage
- Set up CI/CD pipeline for automated deployments
