# ALX Travel App

A Django-based travel application backend that provides RESTful APIs for managing property listings, bookings, and reviews.

## Features

- Property Listings Management
- Booking System
- Review & Rating System
- User Management
- RESTful API with Django REST Framework

## Models

### Listing
- Property information (title, description, type)
- Location details
- Pricing and capacity information
- Host relationship
- Creation and update timestamps

### Booking
- Reservation dates (check-in/check-out)
- Guest information
- Status tracking (pending, confirmed, cancelled, completed)
- Price calculation
- Timestamps

### Review
- Rating system (1-5 stars)
- User comments
- Relationship to listings
- One review per user per listing constraint

## API Serializers

- `UserSerializer`: Basic user information
- `ReviewSerializer`: Review data with reviewer details
- `ListingSerializer`: Complete listing information with host and reviews
- `BookingSerializer`: Booking details with validation

## Database Seeding

The application includes a database seeder that creates:
- Sample users
- Property listings with various types
- Reviews with ratings and comments

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Seed the database:
```bash
python manage.py seed
```

## Technologies Used

- Django
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Python Faker for seed data generation