# Automated Garage Control System with RFID

## Introduction

The Automated Garage Control System is a comprehensive solution for managing car entrances and exits in garages using RFID technology. This fully automated program leverages PyQt5 for the frontend and Django for the backend, offering a centralized control system operated through a network.

## Features

- **Driver and Vehicle Management**: Stores information about drivers, their vehicles, and garage slots.
- **RFID Integration**: Each driver has a unique RFID card used for accessing the garage.
- **Network-Based Control**: Operates across a network, ensuring centralized control and monitoring.
- **Arduino Integration**: Utilizes Arduino for the hardware interface, controlling the physical aspects of the system.
- **Serial Communication**: Employs the serials library for reading RFID input and controlling gates.

## Technology Stack

- **Frontend**: PyQt5
- **Backend**: Django
- **Database**: SQLite(for testing purpose), PostgreSQL(for production) you can find configuration commented
- **Hardware Interface**: Arduino
- **Communication Protocol**: Serials Library for RFID Communication

## Installation

Clone the repository then start the virtual environment.

```bash
# Example installation steps
git clone https://github.com/AnerGcorp/automated-garage-control
cd automated-garage-control

# installation commands for dependencies
python -m virtualenv env
source env/bin/activate
pip install -r requirements
```

## Usage

The first start the backend server

```bash
cd backend/
python manage.py makemigrations api
python manage.py migrate
# Example usage commands
python manage.py runserver
# other necessary commands
```

Then open the new terminal, and go
frontend folder

```bash
cd frontend/
python main.py
```

There is also `rfid-reader` folder there I located the code for arduino file. You can directly upload it into model `Arduino Uno`.

## Contributing

(Instructions for how others can contribute to the project. Include guidelines for code contributions, issue reporting, and pull requests.)

- Fork the repository
- Create your feature branch (`git checkout -b feature/automated-garage-control`)
- Commit your changes (`git commit -am 'Add some Amazing Feature'`)
- Push to the branch (`git push origin feature/automated-garage-control`)
- Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
