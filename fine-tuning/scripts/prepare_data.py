#!/usr/bin/env python3
"""
Data preparation script for fine-tuning.

This script processes raw data into the format required for OpenAI fine-tuning.
It performs validation, formatting, and splitting into training and validation sets.
"""

import os
import json
import argparse
import yaml
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def validate_message(message: Dict[str, str]) -> bool:
    """Validate that a message has the required fields and format."""
    if not isinstance(message, dict):
        return False
    
    required_fields = ['role', 'content']
    for field in required_fields:
        if field not in message:
            return False
    
    valid_roles = ['system', 'user', 'assistant']
    if message['role'] not in valid_roles:
        return False
    
    return True


def validate_example(example: Dict[str, List[Dict[str, str]]]) -> bool:
    """Validate that an example has the correct format for fine-tuning."""
    if 'messages' not in example:
        return False
    
    messages = example['messages']
    if not isinstance(messages, list) or len(messages) < 2:
        return False
    
    for message in messages:
        if not validate_message(message):
            return False
    
    # Check that the conversation alternates between user and assistant
    # (with an optional system message at the start)
    if messages[0]['role'] == 'system':
        start_idx = 1
    else:
        start_idx = 0
    
    for i in range(start_idx, len(messages), 2):
        if i < len(messages) and messages[i]['role'] != 'user':
            return False
        if i+1 < len(messages) and messages[i+1]['role'] != 'assistant':
            return False
    
    return True


def process_raw_data(input_file: str) -> List[Dict[str, Any]]:
    """Process raw data into examples for fine-tuning."""
    examples = []
    
    with open(input_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if validate_example(data):
                    examples.append(data)
                else:
                    print(f"Skipping invalid example: {data}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON line: {line}")
    
    return examples


def split_data(examples: List[Dict[str, Any]], val_ratio: float) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split examples into training and validation sets."""
    random.shuffle(examples)
    split_idx = int(len(examples) * (1 - val_ratio))
    return examples[:split_idx], examples[split_idx:]


def save_jsonl(examples: List[Dict[str, Any]], output_file: str) -> None:
    """Save examples in JSONL format."""
    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')


def main():
    parser = argparse.ArgumentParser(description='Prepare data for fine-tuning')
    parser.add_argument('--input', type=str, required=True, help='Input file or directory')
    parser.add_argument('--output-dir', type=str, default='../data', help='Output directory')
    parser.add_argument('--config', type=str, default='../config/hyperparameters.yaml', help='Config file')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process data
    examples = process_raw_data(args.input)
    print(f"Processed {len(examples)} valid examples")
    
    # Split data
    train_data, val_data = split_data(examples, config['dataset'].get('validation_split', 0.1))
    print(f"Split into {len(train_data)} training examples and {len(val_data)} validation examples")
    
    # Save data
    train_file = output_dir / config['dataset']['training_file']
    val_file = output_dir / config['dataset']['validation_file']
    
    save_jsonl(train_data, train_file)
    save_jsonl(val_data, val_file)
    
    print(f"Saved training data to {train_file}")
    print(f"Saved validation data to {val_file}")


if __name__ == "__main__":
    main() 