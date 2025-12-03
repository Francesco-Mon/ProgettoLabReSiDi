# 📚 Remote Library Management System

**Remote Library System** is a Multithreaded Client-Server application developed in **Python**. It allows users to manage library operations remotely following the **RESTful** architecture paradigm, backed by a **MySQL** database.

This project was developed for the *Network and Distributed Systems Laboratory* course at the **University of Messina**, focusing on raw socket handling, HTTP protocol implementation, and concurrent request management.

---

## ✨ Key Features

The system is designed with a role-based architecture (Admin vs. User) and handles high concurrency.

*   **🔐 Authentication & Security**: User registration and login with password hashing (`bcrypt`).
*   **📡 RESTful Architecture**: Custom implementation of GET, POST, PUT, and DELETE methods handling JSON data.
*   **⚡ Multithreading**: The server uses `ThreadingMixIn` to handle multiple client connections simultaneously without blocking.
*   **👥 Role-Based Access Control (RBAC)**:
    *   **Admins**: Add, update, and delete books from the catalog.
    *   **Users**: Search for books, borrow items, return them, and view personal loan history.
*   **🗄️ Database Integration**: Persistent storage using **MySQL** for books, users, roles, and active loans.
*   **🧪 Stress Testing**: Includes a script to simulate multiple concurrent clients to verify server stability.

## 🛠️ Tech Stack

*   **Language**: Python 3
*   **Database**: MySQL (via `mysql-connector-python`)
*   **Networking**: `http.server`, `socketserver`, `requests`
*   **Concurrency**: Python `threading` module & Locks for thread-safety.
*   **Architecture**: Client-Server (REST API)

## 📂 Project Structure

*   **`Server/`**: Contains the logic to handle HTTP requests, connect to the DB, and manage threads. It automatically initializes the Database schema if missing.
*   **`Client/`**: A CLI (Command Line Interface) application that interacts with the server via HTTP requests.
*   **`Database/`**: SQL logic managed via Python to create tables (`libri`, `utenti`, `prestiti`, `ruoli`).

## 🚀 Installation & Usage

### Prerequisites
*   Python 3.x
*   MySQL Server running locally (default port 3306)
*   Python libraries: `mysql-connector-python`, `requests`, `bcrypt` (if used)

### 1. Setup the Database
Ensure your MySQL server is running. The server script is designed to create the database `biblioteca` and tables automatically upon the first run.
*Check the `db_config` dictionary in the server code to match your MySQL username/password.*

### 2. Start the Server
Navigate to the server directory and run:
```bash
python server.py
```
The server will start listening for HTTP requests on localhost.

### 3. Run the Client
Open a new terminal window and run:
```bash
python client.py
```

Follow the on-screen menu to Register, Login, and interact with the library.

## 📊 Performance & Testing

The project includes a stress-testing module utilizing subprocess to launch multiple client instances simultaneously.
Experimental results demonstrated that the server effectively handles concurrent requests (e.g., 3500+ clients) with stable response times, thanks to the multithreaded implementation.


<p align="center">
Developed by <a href="https://github.com/Francesco-Mon">Francesco Montecucco</a> & <a href="https://github.com/Frankesko">Francesco Bartolomeo</a><br>
 University of Messina
</p>

