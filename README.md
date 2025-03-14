# AgriConnect

AgriConnect is a comprehensive platform designed to connect farmers, buyers, and cooperatives. It provides a marketplace for agricultural products, facilitates communication through a chatbot, and ensures secure transactions. The platform aims to streamline the agricultural supply chain by providing tools for product management, user interaction, and market insights.

## Features

### User Authentication
- **Signup**: Users can create an account by providing their username, email, password, phone number, and role (farmer, buyer, or cooperative).
- **Login**: Users can log in using their email and password.
- **Email Verification**: Users must verify their email address before accessing the platform.
- **Password Reset**: Users can reset their password if they forget it.

### User Roles
- **Farmer**: Can list products for sale, view their profile, manage their products, and access market insights.
- **Buyer**: Can browse products, view seller profiles, interact with the chatbot, rate products, and access a personalized dashboard.
- **Cooperative**: Can manage multiple farmers, list products, communicate with buyers, and access market insights.

### Product Management
- **Add Product**: Farmers and cooperatives can add products with details such as name, description, price, quantity, and media (images/videos).
- **Edit Product**: Users can edit the details of their listed products.
- **Delete Product**: Users can delete their listed products.

### Chatbot Functionality
- **Chatbot Interaction**: Buyers can interact with a chatbot to get information about products.
- **Real-time Responses**: The chatbot provides real-time responses to buyer queries about product details, availability, price, and more.

### Notifications
- **Notifications**: Users receive notifications for important events such as product updates.

### Market Insights
- **Market Insights**: Users can access analytics highlighting top-rated products and farmers, providing valuable market insights.

### Account Management
- **Delete Account**: Users can delete their account from the user profile page.

### Localization
- **Multi-language Support**: The platform supports multiple languages, including English and Kinyarwanda.

## Tools Used

### Django
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.

### Database
- **PostgreSQL**: A powerful, open-source object-relational database system used to store user data, products, messages, and other information.

### Frontend
- **Bootstrap**: A popular CSS framework for developing responsive and mobile-first websites.
- **HTML/CSS**: Standard markup and styling languages used to create the structure and design of the web pages.

### Email
- **SMTP**: Simple Mail Transfer Protocol used to send email verification codes to users.

### Version Control
- **Git**: A distributed version control system used to track changes in the source code during software development.
- **GitHub**: A web-based platform that provides hosting for software development and version control using Git.

### Environment Management
- **Python Virtual Environment (venv)**: A tool to create isolated Python environments, ensuring that dependencies are managed separately for each project.

### Other Tools
- **Mermaid**: A JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions to create and modify diagrams dynamically.
<!-- 
## ER Diagram

```mermaid
erDiagram
    CUSTOMUSER {
        int id
        string username
        string email
        string password
        string role
        bool is_verified
        bool email_verified
    }
    PROFILE {
        int id
        string bio
        string name
        string phone
        string role
        datetime created_at
    }
    VERIFICATIONCODE {
        int id
        string code
        datetime created_at
        datetime expires_at
    }
    PRODUCT {
        int id
        string name
        string contact
        string description
        string media
        decimal price_per_unit
        int quantity_available
        string unit
        float latitude
        float longitude
        datetime created_at
        datetime updated_at
    }
    NOTIFICATION {
        int id
        string message
        datetime timestamp
        bool is_read
    }
    PRODUCTRATING {
        int id
        int rating
    }
    CUSTOMUSER ||--o{ PROFILE : has
    CUSTOMUSER ||--o{ VERIFICATIONCODE : has
    CUSTOMUSER ||--o{ PRODUCT : owns
    CUSTOMUSER ||--o{ NOTIFICATION : receives
    CUSTOMUSER ||--o{ PRODUCTRATING : rates
    PROFILE ||--o{ FARMER : is
    PROFILE ||--o{ BUYER : is
    PROFILE ||--o{ COOPERATIVE : is
    PRODUCT ||--o{ PRODUCTRATING : has
``` -->

## Data Flow Diagram

```mermaid
graph TD
    A[User] -->|Signup/Login| B[Authentication Service]
    B --> C[Database]
    A -->|Browse/Add Products| D[Product Service]
    D --> C
    A -->|Chatbot Interaction| E[Chatbot Service]
    E --> C
    A -->|Receive Notifications| F[Notification Service]
    F --> C
    A -->|Access Market Insights| G[Market Insights Service]
    G --> C
```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/AgriConnect.git
    cd AgriConnect
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- **Access the platform**: Open your browser and go to `http://127.0.0.1:8000/`.
- **Create an account**: Sign up as a farmer, buyer, or cooperative.
- **Verify your email**: Check your email for the verification code and verify your account.
- **List products**: If you are a farmer or cooperative, add products to the marketplace.
- **Browse products**: If you are a buyer, browse the available products and interact with the chatbot for more information.
- **Chatbot**: Use the chatbot functionality to get real-time responses about products.
- **Rate products**: Buyers can rate products they have purchased.
- **Market Insights**: Access analytics to view top-rated products and farmers.

## Contributing

We welcome contributions to AgriConnect! Please follow these steps to contribute:

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m "Add your commit message"
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
6. **Create a pull request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
