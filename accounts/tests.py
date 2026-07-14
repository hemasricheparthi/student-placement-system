"""Basic tests for the placement portal."""
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, Department, Skill
from jobs.resume_matcher import calculate_match, extract_skills_from_text


class ResumeMatcherTests(TestCase):
    def test_extract_skills_from_text(self):
        text = "Experienced in Python, Django, and SQL. Knowledge of Git and Docker."
        skills = extract_skills_from_text(text)
        self.assertIn('Python', skills)
        self.assertIn('Django', skills)

    def test_calculate_match_full(self):
        result = calculate_match(
            ['Python', 'Django', 'SQL'],
            ['Python', 'Django', 'SQL', 'Git'],
        )
        self.assertEqual(result['match_percentage'], 75.0)
        self.assertIn('Git', result['missing_skills'])

    def test_calculate_match_empty_required(self):
        result = calculate_match(['Python'], [])
        self.assertEqual(result['match_percentage'], 100.0)


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        Department.objects.create(name='CSE', code='CSE')

    def test_home_page(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_student_registration_page(self):
        response = self.client.get(reverse('accounts:student_register'))
        self.assertEqual(response.status_code, 200)


class ModelTests(TestCase):
    def test_create_skill(self):
        skill = Skill.objects.create(name='Python', category='LANGUAGE')
        self.assertEqual(str(skill), 'Python')

    def test_create_department(self):
        dept = Department.objects.create(name='Computer Science', code='CS')
        self.assertIn('Computer Science', str(dept))
