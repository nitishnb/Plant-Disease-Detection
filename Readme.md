## Create Flask application

You can choose any directory to create new Flask application. Here i am using below directory to create new Flask project.Create 'plant disease detector' folder
> cd F:\python-projects\flask-projects\plant disease detector

Install virtual environment and create new virtual environment inside project folder
> #install <br>
> pip install virtualenv <br>
> #create virtual environment <br>
> virtualenv project #project is my virtual environment name <br>

Activate virtual environment
> project\Scripts\activate.bat <br>
Install Flask in activated environment <br>
All installation related to this project must be installed in activated environment. 
> pip install Flask <br>

Create app.py file, and other folder as shown [here](https://github.com/nitishnb/Plant-Disease-Detection/blob/main/Plant%20Disease%20Detector/app.py) in plant disease detector folder
### Also add your trained model within the folder 'plant disease detector'

### Run the Flask application
> python app.py

Now you can see the url to your localhost
> http://127.0.0.1:5000/
