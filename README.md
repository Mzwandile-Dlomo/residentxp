# Residentxp - Accommodation Management System

## Overview

Residentxp is designed to streamline the management of accommodations, such as hostels, dormitories, and rental properties. It provides a comprehensive solution for managing room assignments, tenant information, rent collection, maintenance requests, and other essential tasks.

## Features

1. **Room Assignment and Management**
   - Assign rooms to tenants.
   - Track room occupancy status.
   - Manage room details (type, capacity, amenities).

2. **Tenant Management**
   - Maintain tenant profiles (personal details, contact information).
   - Track tenant history and current status.
   - Handle tenant check-ins and check-outs.

3. **Rent Collection**
   - Track rent payments and outstanding balances.
   - Provide payment history and receipts.

4. **Maintenance Management**
   - Submit and track maintenance requests.
   - Assign maintenance tasks to staff.
   - Monitor the status of maintenance activities.

5. **Reporting and Analytics**
   - Generate reports on occupancy rates, rent collection, and maintenance.
   - Analyze trends and generate insights for better decision-making.

6. **Notifications and Alerts**
   - Send automated reminders for rent payments.
   - Notify tenants and staff about maintenance activities.
   - Alert management about important events (e.g., overdue rent).

## Installation

To install the Accommodation Management System, follow these steps:

1. **Clone the repository:**
   ```sh
   
   git clone https://github.com/Mzwandile-Dlomo/residentxp.git
   ```

2. **Navigate to the project directory:**
   ```sh
   cd residentxp
   ```

3. **Install dependencies:**
   ```sh
   pip3 install -r requirements.txt
   ```

4. **Run database migrations:**
   ```sh
   python manage.py makemigration
   python manage.py migrate
   ```

5. **Start the application:**
   ```sh
   python manage.py runserver
   ```

6. **Access the application:**
   - Open your browser and go to `http://localhost:3000`.

## Configuration

The application configuration can be found in the `config` directory. Update the relevant files to match your environment:

- `database.json`: Database connection settings.
- `app.json`: Application-specific settings.

## Usage

1. **Logging In:**
   - Navigate to the login page.
   - Enter your username and password.

2. **Managing Rooms:**
   - Go to the Rooms section.
   - Add, edit, or delete rooms as needed.

3. **Managing Tenants:**
   - Go to the Tenants section.
   - Add, edit, or remove tenant information.
   - Assign tenants to rooms.

4. **Collecting Rent:**
   - Go to the Rent section.
   - Generate invoices and track payments.
   - Send reminders for overdue payments.

5. **Handling Maintenance:**
   - Go to the Maintenance section.
   - Submit new maintenance requests.
   - Assign tasks and monitor their status.

6. **Generating Reports:**
   - Go to the Reports section.
   - Select the type of report you need.
   - Customize the report parameters and generate it.

## Contributing

We welcome contributions to the Accommodation Management System. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```sh
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```sh
   git commit -m "Description of your changes"
   ```
4. Push to your branch:
   ```sh
   git push origin feature-name
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For questions or support, please contact us at support@accommodation-system.com.

---

This readme provides a high-level overview of the Accommodation Management System, including its features, installation instructions, usage guidelines, and contribution process. For more detailed information, refer to the documentation within the project.