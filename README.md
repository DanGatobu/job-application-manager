# Job Application Assistant

## Description
The Job Application Assistant is a web application designed to streamline the job application process. It allows users to store and modify word templates for various job application documents, ultimately creating completed PDF files. This tool aims to simplify and expedite the job application process by providing users with the ability to generate tailored application documents effortlessly.

## Features
- **Template Storage**: Store your job application templates conveniently on the platform.
- **Dynamic Content**: Modify templates to include specific details such as company names, job titles, and more.
- **Automatic PDF Generation**: Generate PDF files from modified templates for easy submission.
- **Email Integration**: Seamlessly send job applications via email directly from the app.
- **Time-Based Messaging**: Customize your application messages based on the time of day.
- **User-Friendly Interface**: Intuitive and easy-to-use interface for a smooth user experience.

## Technologies Used
- Python
- Django (Web Framework)
- HTML/CSS
- Word Automation (via `win32com` for creating PDFs from Word templates)

## How to Use
To run this application locally or deploy it on a server, follow these steps:

1. Clone the repository to your local machine:
git clone <https://github.com/DanGatobu/job-application-manager.git>

2. Install the required Python packages by running:

```pip install -r requirements.txt```

3. Configure the necessary settings in the Django project, such as database settings, email settings, and any other environment variables.

4. Run the Django development server:

```python manage.py runserver```
5. Access the web application by navigating to `http://localhost:8000` in your web browser.

6. Start using the Job Application Assistant to store, modify, and generate job application documents.

## Contributors
- [Dan N. Gatobu](https://github.com/DanGatobu)
