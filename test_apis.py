import os
import django
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['*']

from rest_framework.test import APIClient
from django.core.management import call_command

client = APIClient()

md_content = "# Comprehensive API Request and Response Flow\n\n"

def log_request(method, url, data=None, token=None):
    global md_content
    md_content += f"## {method} {url}\n\n"
    if token:
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    else:
        client.credentials()
        
    md_content += "**Request Data:**\n"
    if data:
        md_content += "```json\n" + json.dumps(data, indent=2) + "\n```\n\n"
    else:
        md_content += "No data\n\n"
    
    if method == 'POST':
        response = client.post(url, data, format='json')
    elif method == 'GET':
        response = client.get(url)
    elif method == 'PUT':
        response = client.put(url, data, format='json')
    elif method == 'PATCH':
        response = client.patch(url, data, format='json')
    elif method == 'DELETE':
        response = client.delete(url)
    
    md_content += "**Response Status:** " + str(response.status_code) + "\n\n"
    md_content += "**Response Body:**\n"
    try:
        if response.content:
            md_content += "```json\n" + json.dumps(response.json(), indent=2) + "\n```\n\n"
        else:
            md_content += "No content\n\n"
    except Exception as e:
        md_content += "```\n" + str(response.content) + "\n```\n\n"
    return response

# Clean DB for fresh start
call_command('flush', '--noinput')

# 1. Accounts
print("Testing Accounts APIs...")
res_reg_inst = log_request('POST', '/api/auth/register/', {
    'username': 'instructor1',
    'password': 'testpassword123',
    'password2': 'testpassword123',
    'email': 'inst1@example.com',
    'role': 'instructor'
})

res_login_inst = log_request('POST', '/api/auth/login/', {
    'username': 'instructor1',
    'password': 'testpassword123'
})
inst_token = res_login_inst.json().get('access') if res_login_inst.status_code == 200 else None

res_reg_stud = log_request('POST', '/api/auth/register/', {
    'username': 'student1',
    'password': 'testpassword123',
    'password2': 'testpassword123',
    'email': 'stud1@example.com',
    'role': 'student'
})

res_login_stud = log_request('POST', '/api/auth/login/', {
    'username': 'student1',
    'password': 'testpassword123'
})
stud_token = res_login_stud.json().get('access') if res_login_stud.status_code == 200 else None

log_request('GET', '/api/auth/users/', token=inst_token)

# 2. Courses
print("Testing Courses APIs...")
res_course = log_request('POST', '/api/course/courses/', {
    'title': 'Test Course',
    'description': 'A course for testing'
}, token=inst_token)
course_id = res_course.json().get('id') if res_course.status_code in [200, 201] else 1

log_request('GET', '/api/course/courses/', token=stud_token)
log_request('GET', f'/api/course/courses/{course_id}/', token=stud_token)
log_request('PATCH', f'/api/course/courses/{course_id}/', {'description': 'Updated description'}, token=inst_token)

res_module = log_request('POST', '/api/course/modules/', {
    'title': 'Test Module',
    'course': course_id,
    'description': 'Test Module Description',
    'order': 1
}, token=inst_token)
module_id = res_module.json().get('id') if res_module.status_code in [200, 201] else 1

log_request('GET', '/api/course/modules/', token=stud_token)
log_request('GET', f'/api/course/modules/{module_id}/', token=stud_token)
log_request('PATCH', f'/api/course/modules/{module_id}/', {'title': 'Updated Module Title'}, token=inst_token)

# 3. Enrolments
print("Testing Enrolments APIs...")
res_enrol = log_request('POST', '/api/enrolment/enrolments/', {
    'course': course_id
}, token=stud_token)
enrol_id = res_enrol.json().get('id') if res_enrol.status_code in [200, 201] else 1

log_request('GET', '/api/enrolment/enrolments/', token=stud_token)
log_request('GET', f'/api/enrolment/enrolments/{enrol_id}/', token=stud_token)

# 4. Submissions
print("Testing Submissions APIs...")
res_sub = log_request('POST', '/api/submissions/submissions/', {
    'module': module_id,
    'content': 'Test submission content'
}, token=stud_token)
sub_id = res_sub.json().get('id') if res_sub.status_code in [200, 201] else 1

log_request('GET', '/api/submissions/submissions/', token=stud_token)
log_request('GET', f'/api/submissions/submissions/{sub_id}/', token=stud_token)
log_request('PATCH', f'/api/submissions/submissions/{sub_id}/', {'content': 'Updated submission content'}, token=stud_token)

# 5. Delete endpoints
print("Testing Delete APIs...")
log_request('DELETE', f'/api/submissions/submissions/{sub_id}/', token=stud_token)
log_request('DELETE', f'/api/enrolment/enrolments/{enrol_id}/', token=stud_token)
log_request('DELETE', f'/api/course/modules/{module_id}/', token=inst_token)
log_request('DELETE', f'/api/course/courses/{course_id}/', token=inst_token)

with open('api_report.md', 'w') as f:
    f.write(md_content)

print("Done. Report saved to api_report.md.")
