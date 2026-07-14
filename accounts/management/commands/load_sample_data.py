"""
Management command to populate sample data for demonstration.
Usage: python manage.py load_sample_data
"""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Announcement, CustomUser, Department, Skill
from companies.models import CompanyProfile
from jobs.models import Application, Job
from placement.models import PlacementDrive
from students.models import StudentProfile


class Command(BaseCommand):
    help = 'Load sample data for the placement portal'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')

        # Departments
        departments = {}
        for name, code in [
            ('Computer Science', 'CSE'),
            ('Information Technology', 'IT'),
            ('Electronics & Communication', 'ECE'),
            ('Mechanical Engineering', 'MECH'),
            ('Electrical Engineering', 'EE'),
        ]:
            dept, _ = Department.objects.get_or_create(
                code=code, defaults={'name': name, 'hod_name': f'Dr. {name} HOD'}
            )
            departments[code] = dept

        # Skills
        skill_names = [
            ('Python', 'LANGUAGE'), ('Java', 'LANGUAGE'), ('JavaScript', 'LANGUAGE'),
            ('Django', 'TECHNICAL'), ('React', 'TECHNICAL'), ('SQL', 'TECHNICAL'),
            ('AWS', 'TOOL'), ('Docker', 'TOOL'), ('Git', 'TOOL'),
            ('Machine Learning', 'TECHNICAL'), ('Data Structures', 'TECHNICAL'),
            ('Communication', 'SOFT'), ('Problem Solving', 'SOFT'), ('Teamwork', 'SOFT'),
            ('Spring Boot', 'TECHNICAL'), ('Node.js', 'TECHNICAL'), ('MongoDB', 'TECHNICAL'),
        ]
        skills = {}
        for name, category in skill_names:
            skill, _ = Skill.objects.get_or_create(
                name=name, defaults={'category': category}
            )
            skills[name] = skill

        # Admin user
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin', email='admin@placement.edu', password='admin123',
                role=CustomUser.Role.ADMIN, first_name='System', last_name='Admin',
            )
            self.stdout.write(self.style.SUCCESS('Created admin (admin/admin123)'))

        # Placement Officer
        if not CustomUser.objects.filter(username='officer').exists():
            CustomUser.objects.create_user(
                username='officer', email='officer@placement.edu', password='officer123',
                role=CustomUser.Role.PLACEMENT_OFFICER, first_name='Placement', last_name='Officer',
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS('Created officer (officer/officer123)'))

        # Sample Students
        students_data = [
            ('student1', 'Rahul', 'Sharma', 'EN2022001', 'CSE', 8.5),
            ('student2', 'Priya', 'Patel', 'EN2022002', 'IT', 7.8),
            ('student3', 'Amit', 'Kumar', 'EN2022003', 'CSE', 9.1),
            ('student4', 'Sneha', 'Reddy', 'EN2022004', 'ECE', 8.0),
            ('student5', 'Vikram', 'Singh', 'EN2022005', 'MECH', 7.5),
        ]
        for username, first, last, enroll, dept_code, cgpa in students_data:
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.create_user(
                    username=username, email=f'{username}@college.edu', password='student123',
                    role=CustomUser.Role.STUDENT, first_name=first, last_name=last,
                    is_verified=True,
                )
                profile = StudentProfile.objects.create(
                    user=user, enrollment_no=enroll, department=departments[dept_code],
                    batch_year=2026, cgpa=cgpa, is_profile_verified=True,
                    placement_status='UNPLACED',
                )
                profile.skills.add(skills['Python'], skills['Java'], skills['SQL'])
                self.stdout.write(f'  Created student: {username}/student123')

        # Sample Companies
        companies_data = [
            ('tcs', 'Tata Consultancy Services', 'IT Services', 'TCS HR', 'hr@tcs.com'),
            ('infosys', 'Infosys Limited', 'IT Services', 'Infosys Recruiter', 'hr@infosys.com'),
            ('wipro', 'Wipro Technologies', 'IT Services', 'Wipro HR', 'hr@wipro.com'),
            ('accenture', 'Accenture', 'Consulting', 'Accenture TA', 'ta@accenture.com'),
        ]
        for username, name, industry, contact, email in companies_data:
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.create_user(
                    username=username, email=email, password='company123',
                    role=CustomUser.Role.COMPANY,
                )
                CompanyProfile.objects.create(
                    user=user, company_name=name, industry=industry,
                    contact_person=contact, contact_email=email,
                    contact_phone='9876543210', is_verified=True, is_active=True,
                    description=f'{name} is a leading company in {industry}.',
                )
                self.stdout.write(f'  Created company: {username}/company123')

        # Sample Jobs
        tcs = CompanyProfile.objects.filter(user__username='tcs').first()
        infosys = CompanyProfile.objects.filter(user__username='infosys').first()
        if tcs and not Job.objects.filter(company=tcs).exists():
            job = Job.objects.create(
                company=tcs, title='Software Engineer',
                description='Looking for talented software engineers with strong programming skills.',
                job_type='FULL_TIME', location='Bangalore', salary_package='6-8 LPA',
                min_cgpa=7.0, max_backlogs=0, experience_required='Fresher',
                vacancies=5, last_date_to_apply=date.today() + timedelta(days=30),
                status='OPEN',
            )
            job.required_skills.add(skills['Python'], skills['Java'], skills['SQL'], skills['Git'])
            job.eligible_departments.add(departments['CSE'], departments['IT'])
            self.stdout.write('  Created TCS Software Engineer job')

        if infosys and not Job.objects.filter(company=infosys).exists():
            job = Job.objects.create(
                company=infosys, title='Full Stack Developer',
                description='Full stack developer role with React and Django experience.',
                job_type='FULL_TIME', location='Hyderabad', salary_package='8-12 LPA',
                min_cgpa=7.5, max_backlogs=0, experience_required='Fresher',
                vacancies=3, last_date_to_apply=date.today() + timedelta(days=45),
                status='OPEN',
            )
            job.required_skills.add(
                skills['Python'], skills['Django'], skills['React'],
                skills['JavaScript'], skills['SQL'],
            )
            job.eligible_departments.add(departments['CSE'], departments['IT'])
            self.stdout.write('  Created Infosys Full Stack Developer job')

        # Placement Drive
        if not PlacementDrive.objects.exists():
            drive = PlacementDrive.objects.create(
                title='Campus Placement Drive 2026',
                description='Annual campus placement drive for final year students.',
                drive_date=date.today() + timedelta(days=60),
                registration_deadline=date.today() + timedelta(days=45),
                venue='Main Auditorium', min_cgpa=6.0, status='UPCOMING',
            )
            if tcs:
                drive.companies.add(tcs)
            if infosys:
                drive.companies.add(infosys)
            drive.departments.add(departments['CSE'], departments['IT'], departments['ECE'])
            self.stdout.write('  Created placement drive')

        # Announcements
        if not Announcement.objects.exists():
            admin = CustomUser.objects.filter(role='ADMIN').first()
            Announcement.objects.create(
                title='Placement Drive 2026 Registration Open',
                content='Registration for the annual campus placement drive is now open. '
                        'All eligible students are requested to complete their profiles.',
                created_by=admin, is_active=True, target_roles='STUDENT',
            )
            Announcement.objects.create(
                title='Resume Upload Mandatory',
                content='All students must upload their resume (PDF format) before applying for jobs.',
                created_by=admin, is_active=True, target_roles='STUDENT',
            )
            self.stdout.write('  Created announcements')

        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Officer:  officer / officer123')
        self.stdout.write('  Student:  student1 / student123')
        self.stdout.write('  Company:  tcs / company123')
