#!/bin/bash

# List of GitHub repositories to download, sorted alphabetically
repositories=(
    "facebookresearch/LASER"
    "huggingface/accelerate"
    "huggingface/datasets"
    "huggingface/evaluate"
    "huggingface/huggingface_hub"
    "huggingface/optimum"
    "huggingface/transformers"
    "microsoft/jarvis"
    "openai/gpt-3"
    "openai/openai-cookbook"
    "openai/openai-python"
    "pytorch/fairseq"
    "pytorch/pytorch"
    "tatsu-lab/stanford_alpaca"
    "tloen/alpaca-lora"
    "Torantulino/Auto-GPT"
)

# Loop through each repository and clone it to a local directory
for repo in "${repositories[@]}"
do
    # Extract the repository name from the URL
    repo_name=$(echo "$repo" | cut -d'/' -f2)
    # Define the path for the local clone of the repository
    repo_path="./$repo_name"
    # Use the Git command line tool to clone the repository
    git clone "https://github.com/$repo.git" "$repo_path"
done
