# Surveillance Sanguine

Surveillance Sanguine is a web application designed to help users upload and monitor blood test results over time. The application categorizes biomarkers to their respective organs or group sets of organs and benchmarks values according to given demographic data. Based on the development or baseline of bespoke biomarkers, the application proposes corrective and preventive measures to improve the health of its users.

## Features

- User registration and authentication
- Upload blood test results
- View and manage uploaded test results
- Monitor biomarkers over time
- Propose health measures based on biomarker data

## Technology Stack

### Backend

- Flask
- SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- Flask-Migrate
- Flask-CORS

### Frontend

- React
- Axios
- React Router DOM

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL

### Backend Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/surveillance-sanguine.git
    cd surveillance-sanguine
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the backend dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and configure the environment variables in a `.env` file:

    ```env
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=postgresql://username:password@localhost:5432/surveillance_sanguine
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

5. Initialize the database:

    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the backend server:

    ```sh
    flask run
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```sh
    cd surveillance-sanguine/frontend
    ```

2. Install the frontend dependencies:

    ```sh
    npm install
    ```

3. Run the frontend development server:

    ```sh
    npm start
    ```

## Usage

1. Open your browser and navigate to `http://localhost:3000` to access the application.
2. Register a new user account or log in with an existing account.
3. Upload blood test results and view the uploaded tests in the dashboard.
4. Monitor the development of biomarkers and receive health recommendations.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
