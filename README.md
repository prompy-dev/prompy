# Prompy
### An interactive prompt coach for learning.

# Fronend Setup


# Backend Setup

### Installation

To start your virtual environment, navigate to `backend` and enter the following commands in your terminal to start the project and install dependencies:

First, activate your virtual environment. From the `backend` dir, enter the following in your terminal:

```shell
source venv/bin/activate

```

Once activated, install all dependencies:
```shell
pip3 install -r requirements.txt

```

Create a `.env` and add the following:
```shell
# Flask configuration
FLASK_APP=app
FLASK_CONFIG=DEV
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_PORT=8080
FLAS_RUN_HOST=0.0.0.0

# Pinecone api key
PINECONE_API_KEY=YOUR_API_KEY

# OpenAI api key
OPENAI_API_KEY=YOUR_API_KEY

```

Run the app!
```
flask run

```