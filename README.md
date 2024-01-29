# 🐾 Pet Project

## Overview 🌟
This project is inspired by the challenges faced by university online systems (like USOS) during peak traffic times, such as when the entire student body is trying to enroll in classes simultaneously. 
The goal is to handle a high volume of requests concurrently, simulating intense traffic scenarios.

## Key Features 🚀
- **Asynchronous Processing**: Leveraging async capabilities to manage concurrent requests efficiently.
- **Django-Ninja**: This is our first project utilizing Django-Ninja for creating fast and easy-to-use APIs.
- **Redis Locking Mechanism**: Implementing a locking mechanism with Redis to prevent duplicate enrollments.
- **Load Testing with Locust**: Utilizing Locust to simulate heavy traffic and test the load capacity of our application.
- **Docker-Compose**: Ensuring easy deployment and management of the application components using Docker-Compose.

## Algorithm 🧠
The core algorithm of this project focuses on performance optimization:
- **Enrollment and State Management in Redis**: We keep all enrollment data and state information during the enrollment process in Redis. This approach significantly reduces database hits and enhances overall performance.

## Setup and Deployment 🛠️
Detailed instructions on setting up and deploying the project will be provided here. This will include steps for using Docker-Compose for a seamless deployment experience.

## Contributing 🤝
We welcome contributions! If you have suggestions or want to improve this project, please feel free to fork the repo and submit a pull request.

## License 📜
This project is open-source and available under the MIT License.
