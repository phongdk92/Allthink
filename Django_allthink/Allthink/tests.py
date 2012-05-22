__author__ = 'Phongdk92'

from django.test import TestCase
from django.test.client import Client


class  TeacherTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_teacher_signup(self):
        data = {
            'username': 'd_k_phong',
            'email': 'phongdk_92@gmail.com',
            'password1': '10020251',
            'password2': '10020251',
            'fullname': 'Do Khac Phong',
        }
        response = self.client.post('/signup/teacher/',data)
        response = self.client.get('/signup/teacher/')
        self.assertContains(response,"Teacher Signup - Fast, Easy, Free")

    def test_teacher_login(self):
        response = self.client.post('/login/',{
            'username':'d_k_phong',
            'password':'10020251'
        })
        self.assertEqual(response.status_code,200)

    def test_teacher_create_lesson(self):
        response = self.client.post('/login/',{
            'username': 'd_k_phong',
            'password': '10020251'
        })
        self.assertEqual(response.status_code,200)
        data = {
            'lessonTitle': 'Math for CS',
            'gradeLevel': 'College',
            'subject': 'Math',
            'description': 'Discrete_mathematics',
        }
        response = self.client.post('/user/d_k_phong/lesson/create/')
        self.assertEqual(response.status_code,302)
        #response = self.client.post('/user/d_k_phong/')
        #self.assertContains(response,"Allthink Lessons",status_code=302)

    def test_teacher_add_video(self):
        response = self.client.post('/login/',{
            'username': 'd_k_phong',
            'password': '10020251'
        })
        self.assertEqual(response.status_code,200)
        data = {
            'pageTitle':'Video Entertainment',
            'url': 'http://www.youtube.com/watch?v=pTp1yHmHi_E',
            'text': 'Davichi & Tara',
        }
        response = self.client.post('/user/d_k_phong/lesson/1/edit/')
        self.assertEqual(response.status_code,302)

    def test_teacher_add_doc(self):
        response = self.client.post('/login/',{
            'username': 'd_k_phong',
            'password': '10020251'
        })
        self.assertEqual(response.status_code,200)
        data = {
            'pageTitle': 'SlideC1-C2',
            'selectFile': '',
            'uploadFile': 'C:\Users\Phongdk92\Desktop\Ke hoach to chuc doi thoai voi dai bieu sinh vien (HKII      nam hoc 2011-2012)(1).doc',
            'text':'Discrete_mathematics',
        }
        response = self.client.post('/user/d_k_phong/lesson/1/add-doc/')
        self.assertEqual(response.status_code,302)

class StudentTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_student_signup(self):
        data = {
            'username': 'phongdk_55',
            'email': 'phongdk_92@gmail.com',
            'password1': '10020251',
            'password2': '10020251',
            'fullname': 'PhongThan',
            }
        response = self.client.post('/signup/student/',data)
        response = self.client.get('/signup/student/')
        self.assertContains(response,"Student Signup - Fast, Easy, Free")

    def test_student_login(self):
        response = self.client.post('/login/',{
            'username':'phongdk_55',
            'password':'10020251'
        })
        self.assertEqual(response.status_code,200)