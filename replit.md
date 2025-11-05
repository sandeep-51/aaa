# ClubConnect - College Club Management Platform

## Overview
ClubConnect is a comprehensive Django-based platform for managing college clubs, events, and student engagement. The platform supports admins, club founders, and students with role-based features.

## Project Structure
- **Django 5.2.7** with Python 3.11
- **Database**: SQLite3 (development), PostgreSQL compatible for production
- **Frontend**: Django templates with Bootstrap
- **Real-time Features**: WebSocket support available for live features

## Recent Changes (November 5, 2025)

### Latest Updates - QR Code Attendance System & Admin Dashboard Complete

#### 🎫 Advanced QR Code Attendance Management (NEW!)
- **Founder-side attendance system** for managing event check-ins
- Founders can now:
  - View all registered students for any event
  - See registration count and check-in status
  - Mark students as attended manually or via QR code
  - Generate individual QR codes for each registered student
- **QR Code scanning workflow**:
  - Students register for events first
  - Founders access "Manage Attendance" page
  - Generate QR code for each student
  - Scan QR code to mark attendance and award points (10 points)
- **Permission system**:
  - Founders, presidents, and vice presidents can manage attendance
  - Only registered students appear in the list
  - Points awarded automatically on check-in
- **Visual feedback**:
  - Color-coded table rows (green for checked-in)
  - Real-time count of registered vs checked-in students
  - Status badges for each student

### Previous Updates - Admin Dashboard Analytics & Club Posting Enhancement

#### 📊 Fixed Admin Dashboard Analytics (NEW!)
- **Fixed analytics charts** to display real data from database
  - User sign-ins chart (last 7 days) - line chart
  - User sign-ups chart (last 7 days) - bar chart
  - Total users, clubs, events, and upcoming events stats cards
- **Added auto-refresh** functionality
  - Dashboard automatically fetches fresh data every 10 minutes (600000ms)
  - Charts and stats update without page reload
  - Uses AJAX to call `/dashboard/ajax/admin_analytics/` endpoint
- **Enhanced UI** with color-coded stat cards
  - Green for Total Users
  - Blue for Total Clubs
  - Red for Total Events
  - Yellow for Upcoming Events

#### 📝 Enhanced Club Posting for Founders
- Club founders can now **post to their club profile** like managing a Facebook page
- Founders can create posts **regardless of membership status**
- "Create Post" button now visible to founders, presidents, and vice presidents outside membership check
- Founders can post:
  - **Events** - event announcements with images
  - **Pictures** - photo posts with captions
  - **General feed** - updates, information, memes
- Posts appear on club profile with:
  - Author information
  - Post type badge
  - Like functionality
  - Images if uploaded

### Previous Updates - Video/Audio Calls & Bug Fixes

#### 🎥 Video and Audio Call Feature (NEW!)
- Implemented **WebRTC-based video/audio calling** for club meetings
- Created `static/js/meeting_room.js` with full meeting room functionality
- Features include:
  - **Live video streaming** with camera access
  - **Audio communication** with microphone access
  - **Toggle video/audio** on/off during meetings
  - **Screen sharing** capability for presentations
  - **Participant list** showing who's in the meeting
  - **Meeting controls** with intuitive UI (mute, video, screen share, end call)
  - **Auto-permission requests** for camera and microphone
- Redesigned meeting room interface with dark theme and professional layout
- No external API keys required - uses native browser WebRTC

#### 🐛 Critical Bug Fixes
1. **Fixed Notification Panel Crash**
   - Resolved "Cannot filter a query once a slice has been taken" error
   - Notifications panel now opens without errors
   - Fixed query ordering in `dashboard/views.py`

2. **Fixed Club Posts Not Saving**
   - Added missing "title" field to post creation form
   - Posts now save correctly and display on club detail page
   - Posts show author, type, content, images, and likes

3. **Restricted Post Creation to Representatives**
   - Only founders, president, and vice-president can create posts
   - Regular members cannot create posts (security improvement)
   - Updated permissions checks in views and templates

4. **Fixed Mentor Session DateTime Warning**
   - Converted naive datetime to timezone-aware datetime
   - Eliminates runtime warnings about timezone support

5. **Event Registration System**
   - Added **event registration** feature for members
   - Members can register for events before attending
   - Shows registration status (Registered/Not Registered)
   - Separate "Register" and "Check In" buttons
   - Notifications sent to founders when members register

#### 📊 Enhanced Founder Dashboard
- Added **Pending Mentor Sessions** section
  - Shows all pending session requests from students
  - Quick link to manage sessions
  - Displays student name, topic, and preferred date

- Added **Pending Feedbacks** section
  - Shows all unreviewed feedback from members
  - Quick link to view and update feedback status
  - Displays feedback type and preview

#### 🎨 UI Improvements
- Fixed notification badge to show actual count (was hardcoded to "3")
- Notifications now highlight unread items with blue background
- Added QR code display on event cards
- Enhanced club detail page with posts and surveys sections
- Fixed notification mark-as-read URL path

#### All Features Now Visible and Functional
- ⭐ Add to Favorites
- 🏆 Leaderboard
- ✏️ Edit Club (founders)
- 📢 Create Announcement (founders)
- 📅 Create Event with QR Code (founders)
- 📊 Create Survey (founders)
- 🎥 Create Meeting with **Video/Audio Calls** (founders) ⭐NEW
- 💬 View Feedbacks (founders)
- 👨‍🏫 Mentor Sessions (founders)
- 💬 Club Chat (members)
- ➕ Create Post (founders/representatives only)
- 💡 Submit Feedback (members)
- 👨‍🏫 Book Mentor Session (members)
- 📅 **Register for Events** (members) ⭐NEW
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
