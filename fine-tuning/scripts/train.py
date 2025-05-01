#!/usr/bin/env python3
"""
Training script for OpenAI fine-tuning.

This script handles the submission of fine-tuning jobs to OpenAI API.
"""

import os
import argparse
import yaml
import time
from pathlib import Path
import datetime
import json
from typing import Dict, Any, Optional

# Import OpenAI only if available
try:
    import openai
    from openai import OpenAI
except ImportError:
    print("Warning: openai package not found. Please install it with: pip install openai")


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def setup_openai_client(config: Dict[str, Any]) -> Any:
    """Setup and return an OpenAI client."""
    api_key = os.environ.get(config['openai']['api_key_env_var'])
    if not api_key:
        raise ValueError(f"OpenAI API key not found in environment variable {config['openai']['api_key_env_var']}")
    
    # Optional org ID
    org_id = os.environ.get(config['openai'].get('organization_env_var', ''), None)
    
    return OpenAI(api_key=api_key, organization=org_id)


def create_finetune_job(
    client: Any,
    training_file_id: str,
    validation_file_id: Optional[str],
    config: Dict[str, Any]
) -> str:
    """Create a fine-tuning job on OpenAI API."""
    model_name = f"{config['model']['name']}"
    if config['model'].get('version'):
        model_name = f"{model_name}-{config['model']['version']}"
    
    job_params = {
        "training_file": training_file_id,
        "model": model_name,
        "hyperparameters": {
            "n_epochs": config['training']['n_epochs'],
            "batch_size": config['training']['batch_size'],
            "learning_rate_multiplier": config['training']['learning_rate_multiplier']
        }
    }
    
    if validation_file_id:
        job_params["validation_file"] = validation_file_id
    
    if config['output'].get('suffix'):
        job_params["suffix"] = config['output']['suffix']
    
    response = client.fine_tuning.jobs.create(**job_params)
    return response.id


def upload_file(client: Any, file_path: str, purpose: str = "fine-tune") -> str:
    """Upload a file to OpenAI API."""
    with open(file_path, "rb") as file:
        response = client.files.create(file=file, purpose=purpose)
    return response.id


def wait_for_file_processing(client: Any, file_id: str, max_wait_sec: int = 60) -> bool:
    """Wait for a file to be processed by OpenAI API."""
    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        file_info = client.files.retrieve(file_id)
        if file_info.status == "processed":
            return True
        print(f"Waiting for file {file_id} to be processed... Status: {file_info.status}")
        time.sleep(5)
    return False


def main():
    parser = argparse.ArgumentParser(description='Run OpenAI fine-tuning')
    parser.add_argument('--config', type=str, default='../config/hyperparameters.yaml', help='Config file')
    parser.add_argument('--training-file', type=str, help='Training data file (overrides config)')
    parser.add_argument('--validation-file', type=str, help='Validation data file (overrides config)')
    parser.add_argument('--job-name', type=str, help='Custom name for the fine-tuning job')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup OpenAI client
    client = setup_openai_client(config)
    
    # Determine file paths
    data_dir = Path('../data')
    training_file = args.training_file or str(data_dir / config['dataset']['training_file'])
    validation_file = args.validation_file or str(data_dir / config['dataset']['validation_file'])
    
    print(f"Using training file: {training_file}")
    if not os.path.exists(training_file):
        raise FileNotFoundError(f"Training file not found: {training_file}")
    
    use_validation = True
    if not os.path.exists(validation_file):
        print(f"Validation file not found: {validation_file}. Proceeding without validation.")
        use_validation = False
    
    # Upload files to OpenAI
    print("Uploading training file...")
    training_file_id = upload_file(client, training_file)
    print(f"Training file uploaded. ID: {training_file_id}")
    
    validation_file_id = None
    if use_validation:
        print("Uploading validation file...")
        validation_file_id = upload_file(client, validation_file)
        print(f"Validation file uploaded. ID: {validation_file_id}")
    
    # Wait for files to be processed
    print("Waiting for files to be processed...")
    if not wait_for_file_processing(client, training_file_id):
        print("Warning: Training file processing timed out, but proceeding anyway.")
    
    if validation_file_id and not wait_for_file_processing(client, validation_file_id):
        print("Warning: Validation file processing timed out, but proceeding anyway.")
    
    # Create fine-tuning job
    print("Creating fine-tuning job...")
    job_id = create_finetune_job(client, training_file_id, validation_file_id, config)
    
    print(f"Fine-tuning job created successfully. Job ID: {job_id}")
    print(f"You can monitor the job status with: python monitor_job.py --job-id {job_id}")
    
    # Save job info
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    job_name = args.job_name or f"finetune_{timestamp}"
    
    models_dir = Path(config['output']['save_dir'])
    models_dir.mkdir(parents=True, exist_ok=True)
    
    job_info = {
        "job_id": job_id,
        "name": job_name,
        "created_at": timestamp,
        "training_file": training_file,
        "training_file_id": training_file_id,
        "validation_file": validation_file if use_validation else None,
        "validation_file_id": validation_file_id,
        "config": config
    }
    
    job_info_file = models_dir / f"{job_name}_info.json"
    with open(job_info_file, 'w') as f:
        json.dump(job_info, f, indent=2)
    
    print(f"Job info saved to {job_info_file}")


if __name__ == "__main__":
    main() 