# This file is for running the application locally

# webpack
npm run-script build
# gunicorn --bind=0.0.0.0 --timeout 600 __main__:application
gunicorn -k tornado main:app
