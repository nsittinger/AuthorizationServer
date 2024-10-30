# OAuth 2.0 Authorization Code Flow - Proof of Concept (PoC)

This project demonstrates the **OAuth 2.0 Authorization Code Grant Flow** using **FastAPI** as the authorization server and **SQLite** as the database. The application is designed to handle user authentication, client authorization, and token generation for secure API access.

## Table of Contents

- [OAuth 2.0 Authorization Code Flow - Proof of Concept (PoC)](#oauth-20-authorization-code-flow---proof-of-concept-poc)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Environment Setup](#environment-setup)
  - [Database Models](#database-models)
  - [Endpoints](#endpoints)
  - [Usage](#usage)
    - [Running the App](#running-the-app)
    - [Authorization Code Flow Walkthrough](#authorization-code-flow-walkthrough)
  - [License](#license)

---

## Project Overview

This project serves as a proof of concept for implementing an OAuth 2.0 Authorization Code Grant flow, a common authorization mechanism that allows clients (applications) to access user data securely. The project enables secure access by managing user sessions, client applications, and authorization codes, and issuing tokens for API access.

## Features

- **User Authentication**: Manage user login and authentication.
- **Client Authorization**: Register and authorize clients to access resources on behalf of users.
- **Authorization Code Flow**: Issue and exchange authorization codes for access tokens.
- **Token Generation and Validation**: Generate and validate access and refresh tokens.
- **Database Support**: SQLite database for managing users, clients, authorization codes, and tokens.

## Getting Started

### Prerequisites

- Python 3.9 or later
- SQLite (included with Python’s standard library)
- Virtual environment setup (recommended)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nsittinger/AuthorizationServer.git
   cd AuthorizationServer
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use `.myenv\Scripts\Activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup

1. **Database Configuration**:
   - The default SQLite database will be created automatically at `auth_database.db`.
2. **Environment Variables**:
   - Create a `.env` file in the project root with any required environment variables (e.g., secret keys).

---

## Database Models

This project uses SQLAlchemy for ORM (Object-Relational Mapping) and defines the following models:

- **User**: Stores user credentials and profile information.
- **Client**: Stores client application details such as `client_id`, `client_secret`, and `redirect_uri`.
- **AuthorizationCode**: Stores authorization codes issued to clients.
- **Token**: Stores access and refresh tokens for client access.
- **Scope**: (Optional) Stores permissions that define client access levels.

## Endpoints

1. **`/authorize`** (GET): Directs the user to authenticate and authorize the client.
2. **`/token`** (POST): Exchanges an authorization code for an access token.
3. **`/login`** (GET/POST): Manages user login for authentication.
4. **`/consent`** (GET/POST): Displays a consent screen for user approval of client scopes.
5. **`/validate-token`** (POST): (Optional) Endpoint to validate the token for secure access to resources.

---

## Usage

### Running the App

1. **Start the FastAPI Application**:

   ```bash
   uvicorn app:app --reload
   ```

2. **Access the API Documentation**:
   - FastAPI provides interactive documentation. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test and explore API endpoints.

### Authorization Code Flow Walkthrough

1. **User Authentication**:

   - Navigate to `/authorize` to start the authorization process. The app will redirect to the login page if the user isn’t authenticated.

2. **Authorization and Consent**:

   - After login, the user is redirected to a consent screen where they approve or deny the client’s requested scopes.

3. **Authorization Code Exchange**:

   - Once consent is granted, the client receives an authorization code. The client can then send a `POST` request to the `/token` endpoint to exchange the code for an access token.

4. **Accessing Protected Resources**:
   - The client uses the access token to request protected resources. Optionally, the `/validate-token` endpoint can be used to verify token validity.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides an overview, setup instructions, and usage guide to help you get started with the OAuth 2.0 Authorization Code Flow PoC. Enjoy exploring OAuth with FastAPI!
