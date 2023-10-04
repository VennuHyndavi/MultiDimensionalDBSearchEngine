# MultiDimensionalDBSearchEngine


Welcome to the Multidimensional Database Search Engine, a powerful tool built with HTML, JavaScript, jQuery, and Python, designed for efficient domain and question exploration. This README provides an overview of the project, highlighting its features and technical architecture.

Features
Dynamic Content Retrieval:

1.The client-side programming involves HTML, JavaScript, and jQuery.
2.AJAX requests interact with the back-end server to fetch information about available domains and questions.
3.Upon page load, a list of domains is retrieved through AJAX and displayed in a select drop-down list.
4.Upon selecting a domain, another AJAX request fetches corresponding questions and their types, which are then displayed using HTML and JavaScript.
5.Questions are paginated for better user experience.


Question Bookmarking:

1.Users can bookmark questions for future reference.
2.A JavaScript/jQuery script facilitates this by making a POST request to an endpoint with a GraphQL mutation.
3.The user's information (userId, domain, questionNumber, question, questionType, options) is stored in a JSON object and sent in the request body.
4.Success and error messages are logged accordingly.


User Management:

1.Users must enter their name before choosing a domain and selecting options.
2.If there is no existing user, a new one is created, and the information is added to the user and user bookmark tables.


Backend

Flask Framework:

1.The server-side is implemented using the Flask framework in Python.
2.Flask is connected to a MySQL service.
3.Graphene-Python package developers are used to build GraphiQL APIs like createUser, searchCriteria, and createUserBookmark.


GraphQL Mutations:

1.CreateUser mutation: Creates a new user, checks if the user already exists, and returns success with the bookmark list.
2.CreateUserBookmark mutation: Creates a new bookmark for a user, checking if the user has already created 5 or more bookmarks.


GraphQL Classes:

Choice, Domain, SearchCriteria, GetResult, Queries, CreateUser, UserBookmarkInput, and CreateUserBookmark are key classes used.


Setup

To run the Multidimensional Database Search Engine:

1.Ensure you have Python and Flask installed.
2.Set up a MySQL service.


Install necessary Python packages using pip install flask graphene.


Usage
Run the Flask app.
Access the application through the provided URL.
