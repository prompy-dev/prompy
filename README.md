# Prompy
### An interactive prompt coach for learning.

### Installation

```shell
npm i
```

### Python virtual environment

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

Once activated, install all dependencies (optional):
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
FLASK_RUN_HOST=0.0.0.0

# Pinecone api key
PINECONE_API_KEY=YOUR_API_KEY

# OpenAI api key
OPENAI_API_KEY=YOUR_API_KEY

```

Run the app!
```
npm run dev

```