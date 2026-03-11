Dhaka Threads | Backend API Architecture
This repository contains the RESTful API powering the Dhaka Threads e-commerce platform. Built with Django and Django REST Framework (DRF), the backend is designed to handle complex relational data, secure user authentication, and optimized product delivery.

View Live API Documentation: https://dhaka-threads-backend.vercel.app/swagger/  
Live Demo: https://dhaka-threads-client.vercel.app/
Frontend Repository: https://github.com/jjannat04/dhaka-threads-client

Technical Specifications
The backend architecture prioritizes data integrity, security, and query performance. It provides a structured interface for the React frontend to consume product data and manage user interactions.
Core Functionality
RESTful Resource Management: Full CRUD capabilities for products, categories, and reviews, organized through decoupled serializers.
JWT Authentication: Secure user sessions implemented via SimpleJWT, providing stateless authentication for reviews and profile management.
Relational Schema Design: An optimized database structure managing One-to-Many (Categories to Products) and Many-to-Many relationships.
Advanced Filtering Engine: Backend-level filtering logic that processes query parameters for size, color, and availability, reducing frontend processing load.
Automated Analytics: Aggregation logic to calculate average ratings and review counts dynamically for each product.
CORS Configuration: Fine-tuned Cross-Origin Resource Sharing settings to ensure secure communication with the React frontend.

Technology Stack
Framework: Django 4+
API Toolkit: Django REST Framework (DRF)
Database: PostgreSQL (Production) / SQLite (Development)
Authentication: JSON Web Tokens (JWT)
Environment Management: Python-decouple / Dotenv
