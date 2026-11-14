# Online Learning Management System (LMS) – Automation Framework

An end-to-end UI and API test automation framework built with **Python**, **Playwright**, and **Pytest**. The suite validates student workflows (login, registration, course discovery, enrollment, progress tracking, and profile management) alongside administrative REST API operations.

---

## Key Features

* **Page Object Model (POM):** Clean separation between UI locators/actions (`pages/`) and test assertions (`tests/ui/`).
* **Built-in Local Mock Server:** Self-contained HTTP mock server in `conftest.py` supporting both HTML UI routes and REST API endpoints without external dependencies.
* **UI & API Test Coverage:** 15 distinct UI test functions (expanding to 18 executed UI items via `@pytest.mark.parametrize`) and 8 API test cases using Playwright's `APIRequestContext`.
* **Network Mocking & Auth Handling:** Demonstrates `page.route()` interception for duplicate enrollment edge cases and global Bearer token injection for API requests.
* **Environment Switching:** Supports `qa` and `staging` configurations via environment variables (`TEST_ENV` and `USE_LIVE_ENV`).
* **Parallel Execution & Retries:** Powered by `pytest-xdist` (`--numprocesses=auto`) and `pytest-rerunfailures` (`--reruns=1`).
* **Rich Reporting & Debugging:** Generates self-contained HTML reports (`pytest-html`), captures failure screenshots, records Playwright traces (`.zip`), logs API request/response payloads, and supports Slack failure notifications.
* **CI/CD Ready:** Automated GitHub Actions workflow (`.github/workflows/playwright.yml`) triggered on pushes and pull requests.

---

## Test Suite Breakdown (26 Total Pytest Items)

* **UI Automation Suite (15 Test Functions / 18 Parameterized Runs):**
  * `tests/ui/test_login.py` — 3 functions (6 runs: valid login, 4 parameterized invalid/empty login validations, and logout).
  * `tests/ui/test_registration.py` — 3 functions (new user registration, mandatory fields, and password mismatch validation).
  * `tests/ui/test_courses.py` — 3 functions (course search, category filtering, and course details view).
  * `tests/ui/test_enrollment.py` — 2 functions (course enrollment and `page.route()` duplicate enrollment handling).
  * `tests/ui/test_profile.py` — 4 functions (profile updates, page navigation, dashboard course list, and student progress tracking).
* **API Automation Suite (8 Test Functions / 8 Runs):**
  * `tests/api/test_get_courses.py` — 2 functions (`GET` all courses `200`, `GET` invalid course ID `404`).
  * `tests/api/test_create_course.py` — 2 functions (`POST` valid course `201`, `POST` invalid payload `422`).
  * `tests/api/test_update_course.py` — 2 functions (`PUT` full update `200`, `PATCH` partial update `200`).
  * `tests/api/test_delete_course.py` — 2 functions (`DELETE` course `204`, `GET` course by valid ID `200`).

---

## Project Structure

```text
LMSAutomation/
│
├── .github/
│   └── workflows/
│       └── playwright.yml          # GitHub Actions CI/CD pipeline
│
├── pages/                          # Page Object Model classes
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── courses_page.py
│   └── profile_page.py
│
├── tests/
│   ├── ui/                         # 15 UI test functions (18 total runs)
│   │   ├── test_login.py
│   │   ├── test_registration.py
│   │   ├── test_courses.py
│   │   ├── test_enrollment.py
│   │   └── test_profile.py
│   │
│   └── api/                        # 8 API test functions
│       ├── test_get_courses.py
│       ├── test_create_course.py
│       ├── test_update_course.py
│       └── test_delete_course.py
│
├── utils/
│   └── test_data.py                # Centralized test data & parameterization sets
│
├── reports/                        # Generated HTML reports and Playwright traces
├── screenshots/                    # Auto-captured screenshots on UI test failures
├── conftest.py                     # Pytest fixtures, local mock server, hooks, and logging
├── pytest.ini                      # Pytest markers and default CLI options
├── requirements.txt                # Project dependencies
└── README.md                       # Setup and execution documentation
```

---

## Prerequisites

* **Python 3.8+** installed and added to your system PATH.
* **Git** for version control and GitHub integration.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd LMS_Automation
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install Playwright browser binaries:**
   ```bash
   playwright install chromium
   ```

5. *(Optional)* **Configure environment variables:**
   Create a `.env` file in the root directory to customize the target environment or enable Slack alerts:
   ```env
   TEST_ENV=qa
   USE_LIVE_ENV=false
   SLACK_WEBHOOK_URL=https://slack.com     # Include slack url if real
   ```

---

## Running Tests

### Run Complete Test Suite (All 26 Items)
Executes all UI and API tests in parallel and generates `reports/report.html`:
```bash
pytest
```

### Run UI Tests Only (Generate Separate UI Report)
```bash
pytest -m ui --html=reports/ui_report.html --self-contained-html
```

### Run API Tests Only (Generate Separate API Report)
```bash
pytest -m api --html=reports/api_report.html --self-contained-html
```

### Run Smoke Suite Only
```bash
pytest -m smoke
```

### Run Regression Suite Only
```bash
pytest -m regression
```

### Switch Between QA and Staging Environments
```bash
# Windows PowerShell
\$env:TEST_ENV="staging"; pytest

# macOS / Linux
TEST_ENV=staging pytest
```

---

## Viewing Reports & Failure Artifacts

* **HTML Reports:** Open `reports/report.html`, `reports/ui_report.html`, or `reports/api_report.html` in any web browser. Click on any API test row to inspect the logged **Request Payload**, **Response Status**, and **Response Body** under the *Captured stdout call* section.
* **Failure Screenshots:** Automatically saved to `screenshots/<test_name>.png` whenever a UI test fails.
* **Playwright Traces:** Saved to `/traces/<test_name>_trace.zip` on failure. Inspect them locally with:
  ```bash
  playwright show-trace reports/traces/<test_name>_trace.zip
  ```
----
## Test Data UI

class TestData:
    VALID_USER = ("srikar", "Test123!")

    INVALID_USERS = [
        ("wrong_user", "Test123!"),
        ("srikar", "wrong_pass"),
        ("", "Test123!"),
        ("srikar", ""),
    ]


-----

## Testdata API
# Course data
COURSES = [
    {"id": 101, "title": "Python Automation", "category": "Development", "status": "Active"},
    {"id": 102, "title": "Playwright Testing", "category": "QA", "status": "Active"},
]

-------
## Output Result:

pytest --headed --slowmo 5000 -n 0                          
============================= test session starts ==============================
platform win32 -- Python 3.13.2, pytest-9.1.1, pluggy-1.7.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.13.2', 'Platform': 'Windows-11-10.0.26300-SP0', 'Packages': {'pytest': '9.1.1', 'pluggy': '1.7.0'}, 'Plugins': {'allure-pytest': '2.16.2', 'html': '4.2.0', 'metadata': '3.1.1', 'playwright': '0.10.0', 'rerunfailures': '16.7', 'xdist': '3.8.0'}}
rootdir: C:\LMSAutomation
configfile: pytest.ini
testpaths: tests
plugins: allure-pytest-2.16.2, html-4.2.0, metadata-3.1.1, playwright-0.10.0, rerunfailures-16.7, xdist-3.8.0
collected 26 items                                                              

tests/api/test_create_course.py::test_create_course PASSED                [  3%]
tests/api/test_create_course.py::test_create_invalid_course PASSED        [  7%]
tests/api/test_delete_course.py::test_delete_course PASSED                [ 11%]
tests/api/test_delete_course.py::test_get_course_by_id PASSED             [ 15%]
tests/api/test_get_courses.py::test_get_all_courses PASSED                [ 19%]
tests/api/test_get_courses.py::test_get_invalid_course PASSED             [ 23%]
tests/api/test_update_course.py::test_put_course PASSED                   [ 26%]
tests/api/test_update_course.py::test_patch_course PASSED                 [ 30%]
tests/ui/test_courses.py::test_search_course[chromium] PASSED             [ 34%]
tests/ui/test_courses.py::test_filter_courses[chromium] PASSED            [ 38%]
tests/ui/test_courses.py::test_open_course_details[chromium] PASSED       [ 42%]
tests/ui/test_enrollment.py::test_enroll_course[chromium] PASSED          [ 46%]
tests/ui/test_enrollment.py::test_duplicate_enrollment[chromium] PASSED   [ 50%]
tests/ui/test_login.py::test_valid_login[chromium] PASSED                 [ 53%]
tests/ui/test_login.py::test_invalid_login[chromium-wrong_user-Pass123!] PASSED [ 57%]
tests/ui/test_login.py::test_invalid_login[chromium-student1-wrong_pass] PASSED [ 61%]
tests/ui/test_login.py::test_invalid_login[chromium--Pass123!] PASSED     [ 65%]
tests/ui/test_login.py::test_invalid_login[chromium-student1-] PASSED     [ 69%]
tests/ui/test_login.py::test_logout[chromium] PASSED                      [ 73%]
tests/ui/test_profile.py::test_update_profile[chromium] PASSED            [ 76%]
tests/ui/test_profile.py::test_page_navigation[chromium] PASSED           [ 80%]
tests/ui/test_profile.py::test_dashboard_courses[chromium] PASSED         [ 84%]
tests/ui/test_profile.py::test_dashboard_progress[chromium] PASSED        [ 88%]
tests/ui/test_registration.py::test_new_registration[chromium] PASSED     [ 92%]
tests/ui/test_registration.py::test_mandatory_fields[chromium] PASSED     [ 96%]
tests/ui/test_registration.py::test_password_mismatch[chromium] PASSED    [100%]

----- Generated html report: file:///C:/LMSAutomation/reports/report.html ------
======================== 26 passed in 304.33s (0:05:04) ========================

