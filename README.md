# Healthcare Operations Management Agent

A sophisticated AI agent for optimizing healthcare facility operations using LangGraph and GPT-4.

## Features

- 🏥 Patient Flow Management 
- 📊 Resource Allocation
- 🎯 Quality Monitoring
- 👥 Staff Scheduling
- 📈 Performance Analytics

## Installation

```bash
# Clone the repository
git clone repository link
cd healthcare-ops-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy example environment file and edit with your settings
cp .env.example .env
```

## Configuration

1. Set up your environment variables in `.env`:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini-2024-07-18
LOG_LEVEL=INFO
```

2. Configure hospital settings in `src/config/settings.py`

## Usage

Basic usage example:

```python
from healthcare_ops_agent import HealthcareAgent

# Initialize agent
agent = HealthcareAgent()

# Process a query
response = agent.process(
    "What is the current ER occupancy and wait time?",
    thread_id="example-thread"
)

print(response)
```

## Project Structure

- `src/`: Main source code
  - `agent.py`: Core agent implementation
  - `config/`: Configuration and settings
  - `models/`: Data models and state management
  - `nodes/`: Graph nodes for different operations
  - `tools/`: Implementation of agent tools
  - `utils/`: Utility functions and helpers
- `tests/`: Test files
- `examples/`: Example usage scripts

## Development

Run tests:
```bash
pytest tests/
```

Format code:
```bash
black src/ tests/
```


