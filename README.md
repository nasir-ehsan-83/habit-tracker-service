# 🌐 Habit Tracker Service & Algorithm Lab

A professional-grade backend service built with **FastAPI** and **MongoDB**, integrated with a curated collection of **Data Structures** and **Algorithm** implementations. This project demonstrates clean code principles, automated testing, and modular software architecture.

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [CS Fundamentals Lab](#-cs-fundamentals-lab)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Testing](#-testing)
- [Author & Support](#-author--support)

## 📊 Project Overview

The **Habit Tracker** is a modular backend application designed to manage and track daily habits. It uses an asynchronous API-first approach with secure authentication and role-based access control.

### Core Features:
* 🔐 **JWT Authentication** with strict Access & Refresh Token rotation.
* 🛡️ **Role-Based Access Control (RBAC)** distinguishing between standard Users and Admins.
* ⚡ **Complete CRUD Operations** for habits, tracking history, and user profiles.
* 🚏 **Rate Limiting & Security** built-in to prevent brute-force and DDoS attacks.
* 📄 **Cursor/Offset Pagination** for handling large datasets efficiently.
* 📝 **Structured Error Logging** for production monitoring and debugging.
* 🚀 **Asynchronous Architecture:** Driven by FastAPI for high-speed request handling.
* 🗄️ **Elegant ODM Integration:** Powered by Beanie with MongoDB for type-safe data modeling.

## 📘 CS Fundamentals Lab

This module contains high-performance implementations of core computer science concepts, serving as a foundational library for the service's logic.

### 🔹 Algorithms
* **Sorting & Searching:** Production-ready implementations of Merge Sort, Quick Sort, and Binary Search.
* **Optimization:** Logic focused on minimizing time complexity \(O(n \log n)\) and reducing memory footprint.

### 🔹 Data Structures
* **Custom Models:** Stacks, Queues, and Linked Lists tailored for non-relational database data flows.
* **Trees:** Hierarchical data structures alongside efficient traversal and search algorithms.

## 🛠 Tech Stack

* **Backend Framework:** Python 3.10+, FastAPI, Beanie-ODM, Pydantic v2
* **Database:** MongoDB
* **Security:** JWT, Bcrypt, SlowAPI (Rate Limiting), CORS Middleware
* **Quality Assurance:** Pytest, Pytest-Asyncio, Coverage.py

## 📁 Project Structure

```text
habit-tracker-service/
├── data_structure_algorithm/
│   ├── algorithms/
│   ├── data_structures/
│   └── tests/
├── habit-tracker/
│   ├── app/
│   │   ├── core/
│   │   ├── db/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── fastapi_offline_docs/
│   └── requirements.txt
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher installed.
* MongoDB server running locally (localhost:27017) or an Atlas URI cloud instance.

### Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd habit-tracker-service/backend
   ```

2. **Establish virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Spin up the service:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Explore interactive API documentation:**
   * Swagger UI: http://localhost:8000/docs
   * ReDoc: http://localhost:8000/redoc

## 🧪 Testing
Automated test suites guarantee database operations and analytical algorithmic modules operate seamlessly.

```bash
# Run all tests sequentially
pytest

# Target testing explicitly at core sorting algorithms
pytest data_structure_algorithm/tests/test_sorting.py

# Check test statement block coverage metrics
pytest --cov=app --cov=data_structure_algorithm --cov-report=term-missing
```

## 👨‍💻 Author
**Nasir Ahmad Ehsan**
* Backend Developer & AI Enthusiast
* GitHub Profile: @nasir-ehsan-83

## ⭐ Support
If this engine accelerated your architecture stack, consider leaving a ⭐ on GitHub!

Built with ❤️ using FastAPI and Beanie ODM
