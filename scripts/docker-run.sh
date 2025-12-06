#!/bin/bash

# Markdown Foldmarks Generator - Docker Wrapper Script (Tree-sitter version)
# This script provides a convenient way to run the foldmarks generator in Docker

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Image name
IMAGE_NAME="foldmarks-generator"
IMAGE_TAG="latest"

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Build Docker image if it doesn't exist
build_image() {
    print_info "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG} (with tree-sitter)..."
    print_info "This may take a few minutes on first build..."
    docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" "$PROJECT_ROOT"
    print_info "Image built successfully!"
}

# Run the Docker container
run_container() {
    local input_file="$1"
    local output_file="$2"
    
    # Get absolute path of current directory
    local workspace_dir="$(pwd)"
    
    docker run --rm \
        -v "${workspace_dir}:/workspace" \
        "${IMAGE_NAME}:${IMAGE_TAG}" \
        "$input_file" ${output_file:+"$output_file"}
}

# Main logic
if [ $# -eq 0 ]; then
    print_error "No arguments provided"
    echo "Usage: $0 <input_file> [output_file]"
    echo ""
    echo "Examples:"
    echo "  $0 index.md                    # Modify input file in place"
    echo "  $0 index.md index_slides.md    # Create new output file"
    echo ""
    echo "Options:"
    echo "  --build    Force rebuild the Docker image"
    exit 1
fi

# Handle --build flag
if [ "$1" == "--build" ]; then
    build_image
    exit 0
fi

# Build image (will use cache if available)
build_image

# Run the container with provided arguments
print_info "Processing markdown file with tree-sitter..."
run_container "$@"

print_info "Done!"
    exit 1
fi

# Handle --build flag
if [ "$1" == "--build" ]; then
    print_info "Forcing image rebuild..."
    docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" "$PROJECT_ROOT"
    print_info "Rebuild complete!"
    exit 0
fi

# Build image if needed
build_image

# Run the container with provided arguments
print_info "Processing markdown file..."
run_container "$@"

print_info "Done!"
