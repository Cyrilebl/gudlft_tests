# Gudlift

This application is a platform dedicated to booking tickets for participation in strength competitions.

The goal is to fix the errors and bugs reported in the Issues section of the [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing) project and implement the requested feature.

## Project Initialization

1. Clone the repository :

```bash
git clone https://github.com/Cyrilebl/gudlft_tests.git
cd gudlft_tests
```

2. Create and activate the virtual environment :

- #### Windows

```bash
python -m venv env
env\Scripts\activate
```

- #### macOS/Linux

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies :

```bash
pip install -r requirements.txt
```

4. Start the server :

```bash
python server.py
```

## External Resources

- [Flask Documentation](https://flask-fr.readthedocs.io/)
- [Coverage Documentation](https://coverage.readthedocs.io/en/7.6.12/)
- [Locust Documentation](https://locust.io/)

## Tests

This project includes several types of tests : unit, integration, functional, and performance tests.

### Running the Tests

```bash
   pytest
```

> ⚠️ **Note:** Before running functional tests with `Selenium`, make sure the server is started.

### Test Coverage

The `Coverage` module is used to analyze test coverage.

Generate a coverage report :

```bash
coverage run -m pytest
coverage report
```

### Performance Tests

Performance tests are conducted using `Locust`.

1. Start Locust

```bash
locust -f tests/performance_tests/locustfile.py
```

2. Access the interface : http://0.0.0.0:8089
3. Enter the application URL in the **"Host"** field (default : http://127.0.0.1:5000/)
4. Configure the other parameters
5. Start the test by clicking the **"Start"** button

## Frequently Asked Questions

If you have any questions, feel free to open a new issue for assistance.
