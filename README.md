# TkinTermPharm - Pharmacy Management System

A modern, enterprise-grade Tkinter-based pharmacy management application with clean architecture, comprehensive features, and professional UI.

## Features

### Core Features
- **User Authentication** - Secure login with role-based access control
- **Dashboard** - Real-time overview and quick statistics
- **User Management** - Complete user lifecycle management
- **Inventory Management** - Track medicines and supplies
- **Sales Management** - Process prescriptions and sales
- **Reporting** - Generate comprehensive reports and analytics
- **Settings** - Application configuration and preferences
- **Audit Logging** - Complete audit trail of all operations

## System Requirements

- Python 3.11 or higher
- SQLite 3.x
- 200 MB disk space
- Windows 7+, macOS 10.12+, or Linux

## Installation

```bash
# Clone repository
git clone https://github.com/Sabarisharjunan/tkinterpharm.git
cd tkinterpharm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/bootstrap.py

# Run application
python -m app.main
```

## Project Structure

See `docs/ARCHITECTURE.md` for detailed information.

```
app/
├── ui/           # Tkinter UI layer
├── services/     # Business logic
├── models/       # Database models
├── repositories/ # Data access layer
├── database/     # Database configuration
├── exceptions/   # Custom exceptions
├── utils/        # Utility functions
├── di/           # Dependency injection
└── state/        # Application state

tests/           # Test suite
docs/            # Documentation
scripts/         # Utility scripts
config/          # Configuration files
data/            # Runtime data
```

## Quick Start

1. Start the application: `python -m app.main`
2. Login with default credentials (see docs/SETUP.md)
3. Navigate using the sidebar
4. Create your first record using the + button

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Format code
black app/
isort app/

# Lint code
flake8 app/
pylint app/

# Security check
bandit -r app/
```

## Documentation

- `docs/ARCHITECTURE.md` - System architecture
- `docs/DATABASE.md` - Database schema
- `docs/API.md` - Service interfaces
- `docs/UI_GUIDE.md` - UI components
- `docs/TESTING.md` - Testing strategy
- `docs/DEPLOYMENT.md` - Deployment guide

## License

MIT License - See LICENSE file

## Support

For issues, questions, or contributions, please visit the GitHub repository.
