
# BloodConnect - Blood Bank Management System

A web-based system built with Django that connects blood donors with people in need of transfusions by location and blood group.

---

## Features

### For Users
- Register as a donor with contact info and blood group
- Create and view blood donation requests
- Filter requests by blood group, state, and city
- Manage personal profile and donation history

### For Admins
- Dashboard overview: donors, requests, and stats
- Manage blood requests and donor listings
- Handle urgent requests

---

## Tech Stack

- **Backend:** Django 5.2.1
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Others:** AJAX for city filtering, Font Awesome for icons

---

## Installation

```bash
git clone https://github.com/OfficialKovid/BloodConnect.git
cd bloodconnect

python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows

pip install -r requirements.txt

python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py runserver
```

---

## Project Structure

```bash
src/
├── apps/
│   ├── accounts/     # User authentication and profiles
│   ├── donors/       # Blood requests and donor management
│   ├── home/         # Static and landing pages
│   └── manager/      # Admin dashboard
├── templates/        # HTML templates
├── static/           # CSS, JS, and images
└── bloodconnect/     # Project settings
```

---

## API Endpoints

- `/login/`, `/signup/`, `/profile/` – User auth & profile
- `/requests/`, `/requests/urgent/`, `/receiver/` – Blood requests
- `/dashboard/` – Admin overview

---

## Database Models

### User
- Full Name, Email, Blood Type
- Phone Numbers, Address, City, State
- `is_active`, `created_at`

### BloodRequest
- Patient Name, Blood Group, Hospital Name
- Required Date, Contact Number
- State, City, Status, Notes

---

## Security

- CSRF protection
- Password hashing
- Session management
- Input validation

---

## Future Enhancements

- SMS/Email alerts for urgent requests
- Donor reward system and analytics
- Mobile app support

---

## License

MIT License © 2025 BloodConnect
