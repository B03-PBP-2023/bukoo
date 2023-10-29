from django.test import TestCase
from .models import Leaderboard
# Create your tests here.

class LeaderboardModelTest(TestCase):
    def test_leaderboard_str(self):
        leaderboard = Leaderboard.objects.create(book="Book Title", userProfile="User Profile", is_recommended=True)
        self.assertEqual(str(leaderboard), "Recommendation by User Profile for Book Title")
