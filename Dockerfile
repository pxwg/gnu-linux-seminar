FROM python:3.11-slim

# Set metadata
LABEL maintainer="your-email@example.com"
LABEL description="Markdown foldmarks generator for Neovim slides with tree-sitter"
LABEL version="2.0"

# Set working directory
WORKDIR /app

# Install build dependencies for tree-sitter
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    tree-sitter \
    tree-sitter-markdown

# Copy the script
COPY scripts/add_foldmarks_treesitter.py /app/add_foldmarks.py

# Make the script executable
RUN chmod +x /app/add_foldmarks.py

# Create a volume mount point for markdown files
VOLUME ["/workspace"]

# Set the working directory to workspace
WORKDIR /workspace

# Set the entrypoint to the script
ENTRYPOINT ["python", "/app/add_foldmarks.py"]

# Default command shows usage
CMD ["--help"]
