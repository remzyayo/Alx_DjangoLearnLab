# Social Media API'

social_media_api

Overview

social_media_api is a Django REST Framework–based backend API for a social media application.
It allows users to register, log in, follow/unfollow others, create and like posts, and receive notifications for interactions like new followers and likes.

This project was built as part of the ALX Django Learn Lab, focusing on practical backend design, RESTful API development, and deployment.


Features
	•	User Management: Register, login, and view profiles.
	•	Follow System: Follow and unfollow users.
	•	Posts: Create, list, and manage user posts.
	•	Likes: Like and unlike posts.
	•	Notifications: Receive notifications for new          followers and likes. 
	•	Secure Authentication: JWT-based authentication for API requests.
	•	Deployment Ready: Configured for production (Gunicorn/Nginx or Heroku).

  Tech Stack
	•	Backend Framework: Django 5.x
	•	API Framework: Django REST Framework
	•	Database: SQLite (development) / PostgreSQL (production)
	•	Authentication: JWT (SimpleJWT)
	•	Server: Gunicorn + Nginx (for production deployment)

    Feature
Endpoint
Method
Description

Register
/api/accounts/register/
POST
Create a new user

Login
/api/accounts/login/
POST
Authenticate a user

Follow User
/api/accounts/follow/<user_id>/
POST
Follow another user

Unfollow User
/api/accounts/unfollow/<user_id>/
POST
Unfollow another user
Create Post
/api/posts/create/
POST
Create a new post

Like Post
/api/posts/<pk>/like/
POST
Like a post

Unlike Post
/api/posts/<pk>/unlike/
POST
Unlike a post

Notifications
/api/notifications/
GET
Retrieve user notifications

Author
Francis Oluremi
