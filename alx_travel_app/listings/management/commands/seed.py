from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Review
from faker import Faker
from decimal import Decimal
import random
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--listings', type=int, default=20, help='Number of listings to create')
        parser.add_argument('--reviews', type=int, default=50, help='Number of reviews to create')

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        # Create users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(options['users']):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            users.append(user)
        
        # Create listings
        self.stdout.write('Creating listings...')
        listings = []
        property_types = [choice[0] for choice in Listing.PROPERTY_TYPES]
        
        for _ in range(options['listings']):
            listing = Listing.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(max_nb_chars=500),
                property_type=random.choice(property_types),
                location=f"{fake.city()}, {fake.country()}",
                price_per_night=Decimal(str(random.uniform(50, 1000))).quantize(Decimal('0.01')),
                bedrooms=random.randint(1, 6),
                bathrooms=random.randint(1, 4),
                max_guests=random.randint(2, 12),
                host=random.choice(users)
            )
            listings.append(listing)

        # Create reviews
        self.stdout.write('Creating reviews...')
        for _ in range(options['reviews']):
            listing = random.choice(listings)
            reviewer = random.choice(users)
            
            # Avoid duplicate reviews from the same user for the same listing
            if not Review.objects.filter(listing=listing, reviewer=reviewer).exists():
                Review.objects.create(
                    listing=listing,
                    reviewer=reviewer,
                    rating=random.randint(1, 5),
                    comment=fake.paragraph()
                )

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(f'Created:')
        self.stdout.write(f'- {options["users"]} users')
        self.stdout.write(f'- {options["listings"]} listings')
        self.stdout.write(f'- {Review.objects.count()} reviews')