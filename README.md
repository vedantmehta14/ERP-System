# ERP System

This project is a comprehensive Enterprise Resource Planning (ERP) system designed to manage and streamline various organizational processes within a single application. Built using Django, this ERP system includes modules for task management, attendance tracking, leave approvals, user management, and more, providing a cohesive platform for improving productivity and operational efficiency.

## Project Overview

The ERP system is a web-based platform developed to handle core business functionalities and reduce the need for multiple software applications. The project incorporates different modules that cater to both employees and administrators, offering features such as task assignment, attendance logging, payslip generation, and event management.

## Features

- **User Authentication**: Secure login, logout, and registration functionalities.
- **Task Management**: Create, assign, and track the status of tasks.
- **Attendance Tracking**: Record daily attendance with detailed logs.
- **Leave Approval**: Submit, review, and approve leave requests.
- **Payslip Generation**: Generate and manage employee payslips.
- **Event Management**: Organize and manage company events.
- **User Management**: Admin functionalities for managing user accounts and roles.
- **Dashboard**: Centralized view for tracking key metrics and notifications.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript, AJAX, jQuery
- **Database**: SQLite (can be configured to other databases as needed)
- **Other Tools**: Bootstrap for UI design

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/vedantmehta14/ERP-System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ERP-System
    ```
3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run database migrations:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```
7. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Log in with the admin or user credentials.
- Use the admin dashboard to manage users, tasks, and other modules.
- Employees can log in to view tasks, mark attendance, request leaves, and access payslips.

## Project Structure

- **`emp_engagement/`**: Contains the main application code, including views, models, and templates.
- **`static/`**: Holds static files like CSS, JavaScript, and images.
- **`templates/`**: Contains HTML templates for rendering pages.
- **`manage.py`**: Django's command-line utility for administrative tasks.

## Key Highlights

- **Modular Design**: Each functionality is developed as a module, allowing easy extension and maintenance.
- **Security**: User authentication and role-based access control.
- **Performance**: Optimized code structure and efficient database queries for scalability.

## Future Enhancements

- Adding more detailed reporting and analytics features.
- Integrating third-party APIs for extended functionalities like email notifications.
- Implementing real-time notifications using WebSockets.

## Contact

For any questions or feedback, feel free to reach out:
- **Author**: Vedant Mehta
- **Email**: mehtavedant8@gmail.com

