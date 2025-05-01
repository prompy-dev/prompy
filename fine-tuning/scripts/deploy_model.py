#!/usr/bin/env python3
"""
Model deployment script.

This script automates the entire workflow of fine-tuning and deploying a model:
1. Runs the fine-tuning process
2. Monitors until completion
3. Updates the application configuration to use the new model
"""

import os
import argparse
import subprocess
import json
import time
import dotenv
from pathlib import Path
import yaml

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_project_root() -> Path:
    """Get the project root directory."""
    # Start from the current script directory and go up to find project root
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent  # From scripts dir to fine-tuning dir to project root
    return project_root

def run_process(command: list) -> tuple:
    """Run a process and return stdout, stderr and return code."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def extract_job_id(output: str) -> str:
    """Extract job ID from training output."""
    # Look for lines containing "Job ID:" and extract the ID
    for line in output.split('\n'):
        if "Job ID:" in line:
            return line.split("Job ID:")[1].strip()
    return None

def extract_model_id(output: str) -> str:
    """Extract model ID from monitoring output."""
    # Look for lines containing "Fine-tuned model:" and extract the ID
    for line in output.split('\n'):
        if "Fine-tuned model:" in line:
            return line.split("Fine-tuned model:")[1].strip()
    return None

def update_env_file(env_file: Path, model_id: str, model_type: str = "parse_query") -> bool:
    """Update the .env file with the new model ID."""
    # Determine the environment variable name based on model type
    if model_type == "parse_query":
        env_var = "PARSE_QUERY_MODEL_ID"
    elif model_type == "chat_llm":
        env_var = "OPENAI_MODEL_ID"
    else:
        env_var = f"{model_type.upper()}_MODEL_ID"
    
    # Create .env file if it doesn't exist
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(f"{env_var}={model_id}\n")
        return True
    
    # Otherwise, update the existing file
    dotenv.load_dotenv(env_file)
    current_value = os.environ.get(env_var)
    
    # Update the .env file
    success = dotenv.set_key(env_file, env_var, model_id)
    
    if success:
        print(f"Updated {env_file} with {env_var}={model_id}")
        if current_value:
            print(f"Previous value was: {current_value}")
    
    return success

def save_model_registry(registry_file: Path, model_info: dict) -> None:
    """Save model information to the registry file."""
    if registry_file.exists():
        with open(registry_file, 'r') as f:
            try:
                registry = json.load(f)
            except json.JSONDecodeError:
                registry = {"models": []}
    else:
        registry = {"models": []}
    
    # Add new model info to the registry
    registry["models"].append(model_info)
    
    # Save updated registry
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"Updated model registry at {registry_file}")

def main():
    parser = argparse.ArgumentParser(description='Deploy a fine-tuned model')
    parser.add_argument('--config', type=str, default='../config/hyperparameters.yaml', help='Config file')
    parser.add_argument('--input', type=str, help='Input data file for training')
    parser.add_argument('--model-type', type=str, default='parse_query', choices=['parse_query', 'chat_llm', 'custom'], help='Type of model to deploy')
    parser.add_argument('--custom-env-var', type=str, help='Custom environment variable name if model-type is custom')
    parser.add_argument('--env-file', type=str, default='.env', help='Environment file to update')
    parser.add_argument('--skip-training', action='store_true', help='Skip training and just deploy an existing model')
    parser.add_argument('--model-id', type=str, help='Model ID to deploy (if skip-training is set)')
    parser.add_argument('--job-id', type=str, help='Job ID to monitor (if skipping initial training)')
    args = parser.parse_args()

    project_root = get_project_root()
    env_file = project_root / args.env_file
    
    # Determine scripts directory
    scripts_dir = Path(__file__).parent
    
    # Load configuration
    config = load_config(scripts_dir.parent / 'config' / 'hyperparameters.yaml')
    
    # Create model registry path
    model_registry = project_root / 'fine-tuning' / 'models' / 'registry.json'
    
    if not args.skip_training and not args.job_id:
        print("=== Starting Fine-Tuning Process ===")
        
        # Prepare data if input is provided
        if args.input:
            prepare_cmd = ['python', str(scripts_dir / 'prepare_data.py'), '--input', args.input]
            print(f"Running: {' '.join(prepare_cmd)}")
            stdout, stderr, ret_code = run_process(prepare_cmd)
            
            if ret_code != 0:
                print("Data preparation failed:")
                print(stderr)
                return
            
            print(stdout)
        
        # Start training
        train_cmd = ['python', str(scripts_dir / 'train.py')]
        if args.config:
            train_cmd.extend(['--config', args.config])
        
        print(f"Running: {' '.join(train_cmd)}")
        stdout, stderr, ret_code = run_process(train_cmd)
        
        if ret_code != 0:
            print("Training failed:")
            print(stderr)
            return
        
        print(stdout)
        
        # Extract job ID
        job_id = extract_job_id(stdout)
        if not job_id:
            print("Could not extract job ID from training output.")
            return
    else:
        job_id = args.job_id
        
    if not args.skip_training:
        # Monitor job
        print(f"=== Monitoring Job {job_id} ===")
        monitor_cmd = [
            'python', 
            str(scripts_dir / 'monitor_job.py'), 
            '--job-id', job_id, 
            '--continuous',
            '--save-model-info'
        ]
        
        print(f"Running: {' '.join(monitor_cmd)}")
        stdout, stderr, ret_code = run_process(monitor_cmd)
        
        if ret_code != 0:
            print("Monitoring failed:")
            print(stderr)
            return
        
        print(stdout)
        
        # Extract model ID
        model_id = extract_model_id(stdout)
        if not model_id:
            print("Could not extract model ID from monitoring output.")
            return
    else:
        if not args.model_id:
            print("Must provide --model-id when using --skip-training")
            return
        model_id = args.model_id
    
    # Update .env file
    print(f"=== Deploying Model {model_id} ===")
    
    # Determine environment variable name
    if args.model_type == 'custom' and args.custom_env_var:
        model_type = args.custom_env_var
    else:
        model_type = args.model_type
    
    # Update environment file
    success = update_env_file(env_file, model_id, model_type)
    
    if not success:
        print(f"Failed to update {env_file}")
        return
    
    # Save to model registry
    model_info = {
        "model_id": model_id,
        "model_type": args.model_type,
        "deployed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_model": config["model"]["name"],
        "job_id": job_id
    }
    
    save_model_registry(model_registry, model_info)
    
    print("=== Deployment Complete ===")
    print(f"Model {model_id} has been deployed for {args.model_type}")
    print(f"To use this model, run your application with the updated environment file: {env_file}")

if __name__ == "__main__":
    main() 