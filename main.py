"""
This file will import the website package.
And grab the create_app function from the __init__.py
To create an application and run.
We are able to do this because website is python package
"""
from website import create_app
app = create_app()
if __name__ == '__main__':
    # To rerun the flask web server every time we make any change to our python code.
    # We use this only during development.
    app.run(debug=True)
