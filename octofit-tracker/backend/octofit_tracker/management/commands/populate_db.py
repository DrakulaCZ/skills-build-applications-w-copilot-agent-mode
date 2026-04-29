from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models

from django.contrib.auth import get_user_model
from django.db import connection

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for test data population
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel_id = db.teams.insert_one({"name": "Marvel"}).inserted_id
        dc_id = db.teams.insert_one({"name": "DC"}).inserted_id

        # Users
        users = [
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team_id": marvel_id},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team_id": marvel_id},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team_id": dc_id},
            {"name": "Batman", "email": "batman@dc.com", "team_id": dc_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {"user_id": user_ids[0], "activity": "Running", "duration": 30},
            {"user_id": user_ids[1], "activity": "Cycling", "duration": 45},
            {"user_id": user_ids[2], "activity": "Swimming", "duration": 60},
            {"user_id": user_ids[3], "activity": "Yoga", "duration": 40},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {"name": "Morning Cardio", "suggested_for": "Marvel"},
            {"name": "Strength Training", "suggested_for": "DC"},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {"user_id": user_ids[0], "points": 100},
            {"user_id": user_ids[1], "points": 90},
            {"user_id": user_ids[2], "points": 95},
            {"user_id": user_ids[3], "points": 80},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
