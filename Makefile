.PHONY: help build run clean test docker-build docker-run docker-clean

# Default target
help:
	@echo "Markdown Foldmarks Generator - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help          - Show this help message"
	@echo "  build         - Build Docker image"
	@echo "  run           - Run the script with Docker (requires INPUT and OUTPUT variables)"
	@echo "  clean         - Remove generated files"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-clean  - Remove Docker image"
	@echo "  test          - Run test with sample file"
	@echo ""
	@echo "Usage examples:"
	@echo "  make build"
	@echo "  make run INPUT=index.md OUTPUT=index_slides.md"
	@echo "  make test"

# Build Docker image
build docker-build:
	@echo "Building Docker image..."
	docker build -t foldmarks-generator:latest .
	@echo "Build complete!"

# Run with Docker (requires INPUT variable)
run docker-run:
ifndef INPUT
	@echo "Error: INPUT variable is required"
	@echo "Usage: make run INPUT=input.md [OUTPUT=output.md]"
	@exit 1
endif
	@echo "Processing $(INPUT)..."
	docker run --rm -v "$$(pwd):/workspace" foldmarks-generator:latest $(INPUT) $(OUTPUT)
	@echo "Done!"

# Clean up Docker image
clean docker-clean:
	@echo "Removing Docker image..."
	-docker rmi foldmarks-generator:latest
	@echo "Cleanup complete!"

# Test with a sample file
test: build
	@echo "Running test..."
	@echo "# Test Document\n\nContent\n\n## Section 1\n\nMore content" > test_input.md
	docker run --rm -v "$$(pwd):/workspace" foldmarks-generator:latest test_input.md test_output.md
	@echo "Test complete! Check test_output.md"
