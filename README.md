# Openex API

## Overview

Openex is an API designed for a stock exchange platform. This application is built using Flask and integrates various extensions and services to provide a comprehensive and robust backend for managing user authentication, transactions, profiles, and more.

## Features

- User authentication and session management
- Database migrations
- Transaction handling
- Profile management
- Localization and translation support
- Email notifications for errors
- Structured logging

## Directory Structure

openex/
│
├── app/
│ ├── init.py
│ ├── auth/
│ ├── errors/
│ ├── main/
│ ├── profile/
│ ├── transactions/
│ ├── models.py
│ └── ...
├── config.py
├── run.py
├── migrations/
├── README.md
└── ...


## Prerequisites

- Python 3.8+
- Flask
- Flask extensions: Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Mail, Flask-Moment, Flask-Babel

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mpereannor/openex.git
    cd openex
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Set up the environment variables:
    ```sh
    export FLASK_APP=openex
    export FLASK_ENV=development
    ```

6. Initialize the database:
    ```sh
    flask db upgrade
    ```

## Configuration

Configuration settings are managed in the `config.py` file. You can create a custom configuration class by extending the base `Config` class and overriding necessary attributes.

## Running the Application

1. Start the Flask application:
    ```sh
    flask run
    ```

2. The application will be available at `http://127.0.0.1:5000/`.

## Blueprints

The application is structured using Flask Blueprints to separate different functionalities:

- **Auth**: Handles user authentication.
- **Errors**: Manages error handling and custom error pages.
- **Main**: The main application logic.
- **Profile**: Manages user profiles.
- **Transactions**: Handles stock exchange transactions.

## Logging

Logging is configured to send error logs via email when the application is in production. Additionally, logging can be configured to write to a rotating file.

## Localization

Localization support is provided using Flask-Babel. The `_l` function is used to mark strings for translation.

## Deployment

For deployment, ensure that the `FLASK_ENV` is set to `production` and configure your web server to serve the application. Detailed instructions for deployment can be found in the Flask documentation.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss potential changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

