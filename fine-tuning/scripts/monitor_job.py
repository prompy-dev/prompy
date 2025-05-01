#!/usr/bin/env python3
"""
Monitoring script for OpenAI fine-tuning jobs.

This script allows tracking the progress of fine-tuning jobs and retrieving metrics.
"""

import os
import argparse
import yaml
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

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


def get_job_info(client: Any, job_id: str) -> Dict[str, Any]:
    """Retrieve information about a fine-tuning job."""
    return client.fine_tuning.jobs.retrieve(job_id)


def get_job_events(client: Any, job_id: str, limit: int = 50) -> list:
    """Retrieve events for a fine-tuning job."""
    return client.fine_tuning.jobs.list_events(
        fine_tuning_job_id=job_id,
        limit=limit
    ).data


def format_job_status(job_info: Dict[str, Any]) -> str:
    """Format job status information for display."""
    status = job_info.status
    created_at = job_info.created_at
    finished_at = getattr(job_info, 'finished_at', None)
    
    base_model = job_info.model
    fine_tuned_model = getattr(job_info, 'fine_tuned_model', None)
    
    status_str = f"Status: {status}\n"
    status_str += f"Created at: {created_at}\n"
    
    if finished_at:
        status_str += f"Finished at: {finished_at}\n"
    
    status_str += f"Base model: {base_model}\n"
    
    if fine_tuned_model:
        status_str += f"Fine-tuned model: {fine_tuned_model}\n"
    
    if hasattr(job_info, 'training_file'):
        status_str += f"Training file: {job_info.training_file}\n"
    
    if hasattr(job_info, 'validation_file') and job_info.validation_file:
        status_str += f"Validation file: {job_info.validation_file}\n"
    
    if hasattr(job_info, 'hyperparameters'):
        status_str += "Hyperparameters:\n"
        # Access safely, handling OpenAI's API changes
        try:
            if hasattr(job_info.hyperparameters, 'n_epochs'):
                status_str += f"  n_epochs: {job_info.hyperparameters.n_epochs}\n"
            if hasattr(job_info.hyperparameters, 'batch_size'):
                status_str += f"  batch_size: {job_info.hyperparameters.batch_size}\n"
            if hasattr(job_info.hyperparameters, 'learning_rate_multiplier'):
                status_str += f"  learning_rate_multiplier: {job_info.hyperparameters.learning_rate_multiplier}\n"
        except Exception as e:
            status_str += f"  Error accessing hyperparameters: {str(e)}\n"
    
    # Add metrics if available
    if hasattr(job_info, 'result_files') and job_info.result_files:
        status_str += "Result files available. Use --download-results to save them.\n"
    
    return status_str


def save_model_info(job_info: Dict[str, Any], output_dir: str) -> None:
    """Save fine-tuned model information to a file."""
    if not hasattr(job_info, 'fine_tuned_model') or not job_info.fine_tuned_model:
        print("No fine-tuned model available yet.")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    model_info = {
        "model_id": job_info.fine_tuned_model,
        "base_model": job_info.model,
        "job_id": job_info.id,
        "created_at": job_info.created_at,
        "finished_at": job_info.finished_at if hasattr(job_info, 'finished_at') else None,
        "status": job_info.status,
        "training_file": job_info.training_file,
        "validation_file": job_info.validation_file if hasattr(job_info, 'validation_file') else None,
    }
    
    # Safely extract hyperparameters
    if hasattr(job_info, 'hyperparameters'):
        hyperparams = {}
        try:
            if hasattr(job_info.hyperparameters, 'n_epochs'):
                hyperparams['n_epochs'] = job_info.hyperparameters.n_epochs
            if hasattr(job_info.hyperparameters, 'batch_size'):
                hyperparams['batch_size'] = job_info.hyperparameters.batch_size
            if hasattr(job_info.hyperparameters, 'learning_rate_multiplier'):
                hyperparams['learning_rate_multiplier'] = job_info.hyperparameters.learning_rate_multiplier
            model_info["hyperparameters"] = hyperparams
        except Exception as e:
            print(f"Warning: Could not serialize hyperparameters: {str(e)}")
    
    # Save to file
    model_file = output_path / f"{job_info.fine_tuned_model.replace(':', '_')}.json"
    with open(model_file, 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"Model information saved to {model_file}")


def monitor_job(client: Any, job_id: str, poll_interval: int = 60, continuous: bool = False) -> None:
    """Monitor a fine-tuning job until completion."""
    first_check = True
    
    while True:
        job_info = get_job_info(client, job_id)
        
        if first_check or job_info.status != "running":
            print("\n" + "="*50)
            print(format_job_status(job_info))
            print("="*50 + "\n")
            first_check = False
        else:
            print(f"Job status: {job_info.status}")
        
        # Get recent events
        events = get_job_events(client, job_id, limit=5)
        if events:
            print("Recent events:")
            for event in reversed(events):  # Show in chronological order
                print(f"  {event.created_at}: {event.message}")
        
        if job_info.status in ["succeeded", "failed", "cancelled"]:
            print(f"Job {job_id} {job_info.status}.")
            return job_info
        
        if not continuous:
            return job_info
        
        print(f"Checking again in {poll_interval} seconds...")
        time.sleep(poll_interval)


def download_result_files(client: Any, job_id: str, output_dir: str) -> None:
    """Download result files from a completed fine-tuning job."""
    job_info = get_job_info(client, job_id)
    
    if not hasattr(job_info, 'result_files') or not job_info.result_files:
        print("No result files available for this job.")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for file_id in job_info.result_files:
        file_info = client.files.retrieve(file_id)
        file_name = file_info.filename
        output_file = output_path / f"{job_id}_{file_name}"
        
        print(f"Downloading {file_name}...")
        content = client.files.content(file_id)
        
        with open(output_file, 'wb') as f:
            f.write(content)
        
        print(f"Saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Monitor OpenAI fine-tuning jobs')
    parser.add_argument('--job-id', type=str, required=True, help='Fine-tuning job ID')
    parser.add_argument('--config', type=str, default='../config/hyperparameters.yaml', help='Config file')
    parser.add_argument('--continuous', action='store_true', help='Monitor continuously until job completes')
    parser.add_argument('--interval', type=int, default=60, help='Polling interval in seconds')
    parser.add_argument('--output-dir', type=str, default='../models', help='Directory to save model info')
    parser.add_argument('--save-model-info', action='store_true', help='Save model info to file when job completes')
    parser.add_argument('--download-results', action='store_true', help='Download result files when job completes')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup OpenAI client
    client = setup_openai_client(config)
    
    # Monitor job
    job_info = monitor_job(client, args.job_id, args.interval, args.continuous)
    
    # Save model info if requested and job is complete
    if args.save_model_info and job_info.status == "succeeded":
        save_model_info(job_info, args.output_dir)
    
    # Download result files if requested
    if args.download_results:
        download_result_files(client, args.job_id, args.output_dir)


if __name__ == "__main__":
    main() 