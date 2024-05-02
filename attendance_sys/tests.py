from django.test import TestCase, Client, SimpleTestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from forms import CreateStudentForm, FacultyForm, StudentForm
from django.urls import reverse, resolve
from .views import *
from models import Faculty, Student, Attendance, Course, Branch, User

User = get_user_model()



class TestForms(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_student_form(self):
        form_data = {
            'user': self.user.id,
            'firstname': 'Om',
            'lastname': 'Kr',
            'roll_num': 'B22CS008',
            'branch': 'CSE',
            'ta': 0,
            'year': '2',
            'course': 'Computer Science',
        }
        form = CreateStudentForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_faculty_form(self):
        form_data = {
            'user': self.user.id,
            'firstname': 'Om',
            'lastname': 'Kr',
            'phone': '9999999999'
        }
        form = FacultyForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_student_form(self):
        form_data = {
            'user': self.user.id,
            'firstname': 'Om',
            'lastname': 'Kr',
            'roll_num': 'B22CS100',
            'branch': 'CSE',
            'ta': 0,
            'year': '2',
            'course': 'Computer Science',
        }
        form = StudentForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.student_home_url = reverse('Student Home')
        self.faculty_home_url = reverse('Faculty Home')
        self.student_login_url = reverse(' Student login')
        self.faculty_login_url = reverse(' Faculty login') 
        self.student_logout_url = reverse('Student logout')
        self.faculty_logout_url = reverse('Faculty logout')

    def test_student_logout_view(self):
        response = self.client.get(reverse('Student logout'))
        self.assertEqual(response.status_code, 302)  

    def test_faculty_logout_view(self):
        response = self.client.get(reverse('Faculty logout'))
        self.assertEqual(response.status_code, 302)  

    def test_student_login_view(self):
        response = self.client.get(self.student_login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance_sys/student_login.html')

    def test_faculty_login_view(self):
        response = self.client.get(self.faculty_login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance_sys/faculty_login.html')


class TestUrls(SimpleTestCase):

    def test_choose_user_url(self):
        url = reverse('Choose User')
        self.assertEqual(resolve(url).func, student_or_faculty_view)
        
    def test_student_home_url(self):
        url = reverse('Student Home')
        self.assertEqual(resolve(url).func, student_home)
        
    def test_faculty_home_url(self):
        url = reverse('Faculty Home')
        self.assertEqual(resolve(url).func, faculty_home)
        
    def test_student_login_url(self):
        url = reverse(' Student login')
        self.assertEqual(resolve(url).func, studentLoginPage)
        
    def test_faculty_login_url(self):
        url = reverse(' Faculty login')
        self.assertEqual(resolve(url).func, facultyLoginPage)
        
    def test_student_logout_url(self):
        url = reverse('Student logout')
        self.assertEqual(resolve(url).func, logoutStudent)
        
    def test_faculty_logout_url(self):
        url = reverse('Faculty logout')
        self.assertEqual(resolve(url).func, logoutFaculty)
        
    def test_student_searchattendance_url(self):
        url = reverse('Student searchattendance')
        self.assertEqual(resolve(url).func, student_searchattendance)
        
    def test_faculty_searchattendance_url(self):
        url = reverse('Faculty searchattendance')
        self.assertEqual(resolve(url).func, faculty_searchattendance)
        
    def test_update_student_redirect_url(self):
        url = reverse('updateStudentRedirect')
        self.assertEqual(resolve(url).func, updateStudentRedirect)
        
    def test_faculty_profile_url(self):
        url = reverse('Faculty account')
        self.assertEqual(resolve(url).func, facultyProfile)
        
    def test_faculty_register_url(self):
        url = reverse('Faculty register')
        self.assertEqual(resolve(url).func, register)
        
    def test_update_student_url(self):
        url = reverse('updateStudent')
        self.assertEqual(resolve(url).func, updateStudent)
        
    def test_attendance_url(self):
        url = reverse('attendance')
        self.assertEqual(resolve(url).func, takeAttendance)
        
    def test_start_attendance_url(self):
        url = reverse('start_attendance', args=['branch', 'year', 'course'])
        self.assertEqual(resolve(url).func, startAttendance)
        
    def test_end_attendance_url(self):
        url = reverse('end_attendance', args=['branch', 'year', 'course'])
        self.assertEqual(resolve(url).func, endAttendance)
        
    def test_video_feed_url(self):
        url = reverse('video_feed')
        self.assertEqual(resolve(url).func, videoFeed)
        
    def test_get_video_url(self):
        url = reverse('videoFeed')
        self.assertEqual(resolve(url).func, getVideo)
        
    def test_download_csv_url(self):
        url = reverse('download_csv', args=['course'])
        self.assertEqual(resolve(url).func, download_csv)
        
    def test_download_excel_url(self):
        url = reverse('download_excel', args=['course'])
        self.assertEqual(resolve(url).func, download_excel)
        
    def test_download_student_csv_url(self):
        url = reverse('download_student_csv', args=['course', 'roll_num'])
        self.assertEqual(resolve(url).func, download_student_csv)
        
    def test_download_student_excel_url(self):
        url = reverse('download_student_excel', args=['course', 'roll_num'])
        self.assertEqual(resolve(url).func, download_student_excel)



class TestModels(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test faculty
        self.faculty = Faculty.objects.create(
            user=self.user,
            firstname='Om',
            lastname='Kr',
            phone='9784512636'
        )

        # Create a test student
        self.student = Student.objects.create(
            user=self.user,
            firstname='Shyam',
            lastname='Kr',
            roll_num='B22CS100',
            branch='CSE',
            year='1',
            course='Computer Science'
        )

        # Create a test attendance
        self.attendance = Attendance.objects.create(
            student=self.student,
            Faculty_Name='Om Kr',
            roll_num='B22CS100',
            branch='CSE',
            year='2',
            course='Computer Science',
            status='Present'
        )

        # Create a test course
        self.course = Course.objects.create(
            code='CSL1010',
            name='Introduction to Computer Science',
            faculty='Om Kr',
            start_time='09:00:00',
            end_time='11:00:00'
        )

        # Create a test branch
        self.branch = Branch.objects.create(
            abbr='CSE',
            branch='Computer Science and Engineering'
        )

    def test_faculty_creation(self):
        self.assertEqual(str(self.faculty), 'Om Kr')

    def test_student_creation(self):
        self.assertEqual(str(self.student), 'B22CS100')

    def test_attendance_creation(self):
        self.assertEqual(str(self.attendance), 'B22CS100_{}_{}'.format(self.attendance.date, self.attendance.course))

    def test_course_creation(self):
        self.assertEqual(str(self.course), 'Introduction to Computer Science : CSL1010')

    def test_branch_creation(self):
        self.assertEqual(str(self.branch), 'Computer Science and Engineering')