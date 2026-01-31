
# LLM Module

This module provides a flexible abstraction layer for integrating multiple AI/LLM backends into the application.

## Overview

The LLM module is designed with extensibility in mind, allowing you to easily add new AI agents without modifying existing code. It follows a backend pattern where each AI provider is implemented as a separate backend.

## Architecture

### Backends

Backends are individual implementations for different AI providers (e.g., OpenAI, Anthropic, local models). Each backend:

- Implements a common interface
- Handles provider-specific authentication and API calls
- Normalizes responses to a consistent format

To add a new backend:

1. Create a new file in the `backends/` directory
2. Implement the required interface methods
3. Register the backend in the service layer

### Prompts

The `prompts.py` file centralizes all prompt templates used across the application. This approach:

- Keeps prompts organized and maintainable
- Allows easy A/B testing and iteration
- Separates prompt engineering from business logic
- Enables version control of prompt changes

### Service Layer

The service file acts as the main interface for the LLM module. It:

- Abstracts backend selection logic
- Provides a unified API for the rest of the application
- Handles backend initialization and configuration
- Routes requests to the appropriate backend
- Switch between AI backends without changing application code

## Usage

```python
from app.llm.service import LLMService

# Initialize service with desired backend
service = LLMService(backend="openai")

# Use the service
response = service.generate(prompt="Your prompt here")
```
