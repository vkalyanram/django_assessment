# Django Assessment - Accuknox

This repository contains solutions for Django Trainee Assessment at Accuknox, organized in a proper Django project format.


## Requirements
- Python 3.8+
- Django 5.0+


## Project Setup
1.  **Clone/Navigate to Project Directory**:
    ```bash
    cd django_assessment
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**:
    ```bash
    python -m venv venv
    ```

3.  **Activate Virtual Environment**:
    - Windows:
      ```bash
      venv\Scripts\activate
      ```
    - macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


## Project Structure
```
django_assessment/
├── manage.py                  # Django management script
├── requirements.txt            # Project dependencies
├── rectangle_project/        # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Project settings (custom_shapes app added to INSTALLED_APPS)
│   ├── urls.py
│   └── wsgi.py
├── custom_shapes/         # Django app containing all solutions
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── rectangle.py      # Solution: Custom Rectangle Class
│   ├── signals_q1.py    # Solution: Q1 - Django Signals Sync/Async
│   ├── signals_q2.py    # Solution: Q2 - Django Signals Same Thread
│   ├── signals_q3.py    # Solution: Q3 - Django Signals Same Transaction
│   ├── tests.py
│   └── views.py
├── test_rectangle.py      # Test script for Rectangle class
└── README.md
```


## Solutions Overview

---

### Topic: Custom Classes in Python - Rectangle Class
**File**: `custom_shapes/rectangle.py`

**Requirements**:
1.  Instance requires `length: int` and `width: int` to initialize
2.  Instance is iterable
3.  Iteration yields `{'length': <value>}` followed by `{'width': <value>}`

**How to test**:
```bash
python test_rectangle.py
```
Or in Django shell:
```python
python manage.py shell
from custom_shapes.rectangle import Rectangle
rect = Rectangle(10, 5)
for item in rect:
    print(item)
```

---

### Topic: Django Signals

#### Question 1: Synchronous or Asynchronous?
**Answer**: By default, Django signals are executed **synchronously** (blocking).
- When you call `signal.send()`, all connected receiver functions run immediately, sequentially, and block the caller until all receivers finish.

**File**: `custom_shapes/signals_q1.py`
**How to run**:
```bash
python -m custom_shapes.signals_q1
```

---

#### Question 2: Same Thread as Caller?
**Answer**: Yes, Django signals run in **the same thread** as the caller by default.

**File**: `custom_shapes/signals_q2.py`
**How to run**:
```bash
python -m custom_shapes.signals_q2
```

---

#### Question 3: Same Database Transaction?
**Answer**: Yes, by default Django signals run in **the same database transaction** as the caller.
- If the caller's transaction rolls back, any database changes made by signal handlers are also rolled back.

**File**: `custom_shapes/signals_q3.py`
**How to run**:
```bash
python -m custom_shapes.signals_q3
```
