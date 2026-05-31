# Employee Scheduling System

Employee Scheduling System is a Flask-based web application that allows managers to manage employees and assign work shifts.

## Features

- User registration and login
- Employee management
  - Add employees
  - View employees
  - Edit employees
  - Delete employees
- Shift management
  - Add shifts
  - View shifts
  - Edit shifts
  - Delete shifts
- Shift validation
  - Prevents duplicate shifts for the same employee on the same date
  - Ensures end time is after start time
- Dashboard statistics
  - Total employees
  - Total shifts
- Flash messages for user feedback
- SQLite database integration

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- Jinja Templates
- Git & GitHub

## Project Purpose

The purpose of this project is to create a simple employee scheduling system where a manager can organize staff information and work schedules efficiently.

## User Stories

### US1 - Employee Management
A manager can create, view, update, and delete employees.

### US2 - Shift Management
A manager can assign, view, update, and delete shifts for employees.

### US3 - Validation System
The system validates shift data to prevent scheduling errors.

### US4 - Dashboard & Statistics
A manager can view basic statistics about employees and shifts.

### US5 - System Navigation and User Interface
The application provides a simple and consistent interface for navigation.

## How to Run

1. Clone the repository

```bash
git clone https://github.com/q5f62p4nw7-blip/employee-scheduling.git