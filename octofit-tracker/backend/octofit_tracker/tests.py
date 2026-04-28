from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
        self.assertEqual(user.username, 'testuser')

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(username='member', email='member@example.com', first_name='Member', last_name='Test')
        team = Team.objects.create(name='TeamA')
        team.members.add(user)
        self.assertIn(user, team.members.all())

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        activity = Activity.objects.create(name='Running', description='Run fast!')
        self.assertEqual(activity.name, 'Running')

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        user = User.objects.create(username='workoutuser', email='workout@example.com', first_name='Workout', last_name='User')
        activity = Activity.objects.create(name='Cycling')
        workout = Workout.objects.create(user=user, activity=activity, duration=30, calories_burned=200)
        self.assertEqual(workout.duration, 30)

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        user = User.objects.create(username='leader', email='leader@example.com', first_name='Lead', last_name='Board')
        leaderboard = Leaderboard.objects.create(user=user, total_points=100, rank=1)
        self.assertEqual(leaderboard.rank, 1)
