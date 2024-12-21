# Flavia

Disclaimer: This project is in progress! Lots of functionalities doesn't work yet. But, im open for your opinion.

Flavia is a boilerplate combining Flask and Vue, offering a ready-to-use system for authentication, user management, and permissions. The goal of the project is to provide a solid foundation for building web applications without starting from scratch.

## Features

### Backend (Flask):
- **Authentication and Authorization**
  - Login system based on Flask-Login.
  - Session management and handling roles and permissions.
- **User Management**
  - Adding, editing, and deleting users.
  - Assigning roles and permissions.
- **Database Management**
  - Using Flask-SQLAlchemy as the ORM.
  - Database migrations with Flask-Migrate and Alembic.
  - Data serialization with Flask-Marshmallow and Marshmallow-SQLAlchemy.
- **Localization and Internationalization**
  - Multilingual support using Flask-Babel.
- **Email Notifications**
  - Built-in email support using Flask-Mail and email-validator.
- **CORS Support**
  - Flask-CORS configuration for cross-origin communication.
- **Admin Interface**
  - User-friendly admin panel powered by Flask-Admin.

### Frontend (Vue):
- **Modularity**
  - Vue built with Vite, enabling fast application development.
- **Styling**
  - Using Bulma CSS for responsive user interfaces.
- **Integrated Views**
  - Login and registration pages.
  - Admin panel for managing users and roles.

## Requirements

- **Python 3.8+**
- **Node.js 16+**
- **MariaDB/MySQL** (or other compatible databases)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/flavia.git
   cd flavia
   ```

2. **Install backend dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

4. **Configure the database:**
   - Create a `.env` file based on `.env.example` and fill in the database details.
   - Initialize the database:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

5. **Run the application:**
   ```bash
   flask run
   ```

## Project Structure

```
flavia/
├── application/        # Main backend code
├── frontend/           # Vue application source code
├── migrations/         # Migration files
├── .env.example        # Example configuration file
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Future Enhancements
- API for communication between frontend and backend.
- Additional views for more complex applications.
- Integration with external services (e.g., Stripe, AWS S3).

## License
The Flavia project is available under the MIT license.

---

Have questions? Report issues or suggest enhancements in the Issues section on GitHub!
