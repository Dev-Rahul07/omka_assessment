# Comprehensive API Request and Response Flow

## POST /api/auth/register/

**Request Data:**
```json
{
  "username": "instructor1",
  "password": "testpassword123",
  "password2": "testpassword123",
  "email": "inst1@example.com",
  "role": "instructor"
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "user": {
    "id": 1,
    "username": "instructor1",
    "email": "inst1@example.com",
    "role": "instructor",
    "first_name": "",
    "last_name": ""
  }
}
```

## POST /api/auth/login/

**Request Data:**
```json
{
  "username": "instructor1",
  "password": "testpassword123"
}
```

**Response Status:** 200

**Response Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NTkyMDM1MSwiaWF0IjoxNzg1MzE1NTUxLCJqdGkiOiIyMmY4NzE5ODcwYmE0M2Q5YjNlYWQ2MzRhZTM5NWU0MCIsInVzZXJfaWQiOiIxIn0.nYW7uDTyJ5eakYO3lMM2RfIzLoYVnBFccwBDlPpd1PU",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1NDAxOTUxLCJpYXQiOjE3ODUzMTU1NTEsImp0aSI6IjQ5YzQzZDFjNTRkNzQyMjA5YjM5OTQ2YWJjOWNlNzdmIiwidXNlcl9pZCI6IjEifQ.1FCvzQAiBHv1v96uGcFs7-yvfjGt08MXW70_2TAJxWQ",
  "user": {
    "id": 1,
    "username": "instructor1",
    "email": "inst1@example.com",
    "role": "instructor"
  }
}
```

## POST /api/auth/register/

**Request Data:**
```json
{
  "username": "student1",
  "password": "testpassword123",
  "password2": "testpassword123",
  "email": "stud1@example.com",
  "role": "student"
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "user": {
    "id": 2,
    "username": "student1",
    "email": "stud1@example.com",
    "role": "student",
    "first_name": "",
    "last_name": ""
  }
}
```

## POST /api/auth/login/

**Request Data:**
```json
{
  "username": "student1",
  "password": "testpassword123"
}
```

**Response Status:** 200

**Response Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4NTkyMDM1MiwiaWF0IjoxNzg1MzE1NTUyLCJqdGkiOiI1ZDgwMGIyODIwM2M0NzkxOTJhODY5NTJjNTc5ZTk3YyIsInVzZXJfaWQiOiIyIn0.1qPGFbch_I8zIrldtBI328wDOKZx5276v4EOziQAWLE",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1NDAxOTUyLCJpYXQiOjE3ODUzMTU1NTIsImp0aSI6ImQ2ZGU2MjRlMWEzZjRhYjc4MDJiNjU0NzY5Y2I0Njg1IiwidXNlcl9pZCI6IjIifQ.3xNTdvbN8cd_kuA0gAUHK2TNNrmQFWJJT1lTKg99Ql4",
  "user": {
    "id": 2,
    "username": "student1",
    "email": "stud1@example.com",
    "role": "student"
  }
}
```

## GET /api/auth/users/

**Request Data:**
No data

**Response Status:** 403

**Response Body:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

## POST /api/course/courses/

**Request Data:**
```json
{
  "title": "Test Course",
  "description": "A course for testing"
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "id": 1,
  "title": "Test Course",
  "description": "A course for testing",
  "instructor": "instructor1",
  "modules": [],
  "created_at": "2026-07-29T08:59:12.627220Z",
  "updated_at": "2026-07-29T08:59:12.627238Z"
}
```

## GET /api/course/courses/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
[
  {
    "id": 1,
    "title": "Test Course",
    "description": "A course for testing",
    "instructor": "instructor1",
    "modules": [],
    "created_at": "2026-07-29T08:59:12.627220Z",
    "updated_at": "2026-07-29T08:59:12.627238Z"
  }
]
```

## GET /api/course/courses/1/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "title": "Test Course",
  "description": "A course for testing",
  "instructor": "instructor1",
  "modules": [],
  "created_at": "2026-07-29T08:59:12.627220Z",
  "updated_at": "2026-07-29T08:59:12.627238Z"
}
```

## PATCH /api/course/courses/1/

**Request Data:**
```json
{
  "description": "Updated description"
}
```

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "title": "Test Course",
  "description": "Updated description",
  "instructor": "instructor1",
  "modules": [],
  "created_at": "2026-07-29T08:59:12.627220Z",
  "updated_at": "2026-07-29T08:59:12.649029Z"
}
```

## POST /api/course/modules/

**Request Data:**
```json
{
  "title": "Test Module",
  "course": 1,
  "description": "Test Module Description",
  "order": 1
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "id": 1,
  "course": 1,
  "title": "Test Module",
  "description": "Test Module Description",
  "order": 1,
  "created_at": "2026-07-29T08:59:12.660564Z",
  "updated_at": "2026-07-29T08:59:12.660582Z"
}
```

## GET /api/course/modules/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
[
  {
    "id": 1,
    "course": 1,
    "title": "Test Module",
    "description": "Test Module Description",
    "order": 1,
    "created_at": "2026-07-29T08:59:12.660564Z",
    "updated_at": "2026-07-29T08:59:12.660582Z"
  }
]
```

## GET /api/course/modules/1/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "course": 1,
  "title": "Test Module",
  "description": "Test Module Description",
  "order": 1,
  "created_at": "2026-07-29T08:59:12.660564Z",
  "updated_at": "2026-07-29T08:59:12.660582Z"
}
```

## PATCH /api/course/modules/1/

**Request Data:**
```json
{
  "title": "Updated Module Title"
}
```

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "course": 1,
  "title": "Updated Module Title",
  "description": "Test Module Description",
  "order": 1,
  "created_at": "2026-07-29T08:59:12.660564Z",
  "updated_at": "2026-07-29T08:59:12.676256Z"
}
```

## POST /api/enrolment/enrolments/

**Request Data:**
```json
{
  "course": 1
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "id": 1,
  "student": "student1",
  "course": 1,
  "course_title": "Test Course",
  "enrolled_at": "2026-07-29T08:59:12.685363Z"
}
```

## GET /api/enrolment/enrolments/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
[
  {
    "id": 1,
    "student": "student1",
    "course": 1,
    "course_title": "Test Course",
    "enrolled_at": "2026-07-29T08:59:12.685363Z"
  }
]
```

## GET /api/enrolment/enrolments/1/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "student": "student1",
  "course": 1,
  "course_title": "Test Course",
  "enrolled_at": "2026-07-29T08:59:12.685363Z"
}
```

## POST /api/submissions/submissions/

**Request Data:**
```json
{
  "module": 1,
  "content": "Test submission content"
}
```

**Response Status:** 201

**Response Body:**
```json
{
  "id": 1,
  "student": "student1",
  "module": 1,
  "module_title": "Updated Module Title",
  "content": "Test submission content",
  "submitted_at": "2026-07-29T08:59:12.706464Z",
  "updated_at": "2026-07-29T08:59:12.706483Z"
}
```

## GET /api/submissions/submissions/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
[
  {
    "id": 1,
    "student": "student1",
    "module": 1,
    "module_title": "Updated Module Title",
    "content": "Test submission content",
    "submitted_at": "2026-07-29T08:59:12.706464Z",
    "updated_at": "2026-07-29T08:59:12.706483Z"
  }
]
```

## GET /api/submissions/submissions/1/

**Request Data:**
No data

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "student": "student1",
  "module": 1,
  "module_title": "Updated Module Title",
  "content": "Test submission content",
  "submitted_at": "2026-07-29T08:59:12.706464Z",
  "updated_at": "2026-07-29T08:59:12.706483Z"
}
```

## PATCH /api/submissions/submissions/1/

**Request Data:**
```json
{
  "content": "Updated submission content"
}
```

**Response Status:** 200

**Response Body:**
```json
{
  "id": 1,
  "student": "student1",
  "module": 1,
  "module_title": "Updated Module Title",
  "content": "Updated submission content",
  "submitted_at": "2026-07-29T08:59:12.706464Z",
  "updated_at": "2026-07-29T08:59:12.724444Z"
}
```

## DELETE /api/submissions/submissions/1/

**Request Data:**
No data

**Response Status:** 204

**Response Body:**
No content

## DELETE /api/enrolment/enrolments/1/

**Request Data:**
No data

**Response Status:** 204

**Response Body:**
No content

## DELETE /api/course/modules/1/

**Request Data:**
No data

**Response Status:** 204

**Response Body:**
No content

## DELETE /api/course/courses/1/

**Request Data:**
No data

**Response Status:** 204

**Response Body:**
No content

