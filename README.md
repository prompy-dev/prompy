# Prompy
## An interactive prompt coach for learning

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.x
- Git

### Installation and Setup

1. **Clone the repository**
   ```shell
   git clone https://github.com/yourusername/prompy.git
   cd prompy
   ```

2. **Install Node dependencies**
   ```shell
   npm install
   ```

3. **Create and activate Python virtual environment**
   
   Create and setup the virtual environment with all dependencies:
   ```shell
   npm run py-venv
   ```
   
   This command will:
   - Create a virtual environment in the `venv` directory
   - Activate the virtual environment
   - Install all Python dependencies listed in `requirements.txt`
   
   If you need to manually activate the virtual environment later:
   
   On macOS/Linux:
   ```shell
   source venv/bin/activate
   ```
   
   On Windows:
   ```shell
   venv\Scripts\activate
   ```

4. **Environment Configuration**

   Create a `.env` file in the project root and add the following:
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
   
   Make sure to replace `YOUR_API_KEY` with your actual API keys for Pinecone and OpenAI.

5. **Running the Application**

   Start both the Next.js frontend and Flask backend:
   ```shell
   npm run dev
   ```
   
   If you need to run only the Flask API:
   ```shell
   npm run flask-dev
   ```
   
   If you need to run only the Next.js frontend:
   ```shell
   npm run next-dev
   ```

6. **Accessing the Application**

   The frontend will be available at: http://localhost:3000
   
   The Flask API will be available at: http://localhost:8080

### Troubleshooting

- If you encounter issues with the virtual environment, try removing the `venv` directory and creating it again:
  ```shell
  rm -rf venv
  npm run py-venv
  ```

- If you see dependency-related errors, make sure both npm packages and Python requirements are installed:
  ```shell
  npm install
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```
