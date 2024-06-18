# Directory Structure
__init__.py: Initializes the myapp package. This file is required to treat the directory as a package.

app.py: The main application script that sets up the Flask web application, routes, and server configuration. It handles user requests and responses.

forms.py: Contains the form classes for handling user input. Defines the structure and validation for input forms used in the application.

models.py: Defines the data models and database schema for the application. Manages data storage and retrieval.

routes.py: Contains the route handlers for the web application. Maps URLs to specific functions in the application.

scheduler.py: Implements the core scheduling algorithms and logic. Processes user input to generate an optimal class schedule.

static/: Directory for static files such as CSS, JavaScript, and images. These files are served directly to the client's browser.

templates/: Directory for HTML templates. Contains the HTML files used to render the web pages for the application.

utils.py: Contains utility functions used throughout the application. Provides helper functions for various tasks.
