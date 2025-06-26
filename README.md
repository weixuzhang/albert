# AI Agent Sandbox Prototype

A modular, clearly structured sandbox prototype integrating multiple AI agents—Albert Core, Planning Agent, and Questioning Agent—to facilitate dynamic, interactive user experiences.

## 🏗️ Project Structure

```
albert/
├── instructions.md              # Project specification
├── README.md                   # This file
├── conda-setup.md              # Conda environment setup guide
├── environment.yml             # Conda environment configuration
├── requirements.txt            # Pip dependencies (for venv option)
├── config.py                   # System configuration and prompts
├── openai_utils.py             # OpenAI API utilities
├── setup_openai.py             # OpenAI setup script
├── main.py                     # Demo script
├── test_openai_integration.py  # OpenAI integration tests
├── json_schemas.py             # JSON structure standards
├── albert_core.py              # Albert Core agent
├── planning_agent.py           # Planning agent
├── questioning_agent.py        # Questioning agent (slot filler)
├── orchestrator.py             # Central coordinator
├── test_albert_core.py         # Albert Core tests
├── test_planning_agent.py      # Planning Agent tests
├── test_questioning_agent.py   # Questioning Agent tests
└── test_orchestrator.py        # Orchestrator tests
```

## 🤖 Agents Overview

### 1. Albert Core
- **Role**: Main user-facing interface
- **Responsibilities**: 
  - Receive and process initial user inputs
  - Provide immediate responses or preliminary processing
  - Categorize requests for appropriate handling

### 2. Planning Agent
- **Role**: Strategic plan formulation
- **Responsibilities**:
  - Analyze Albert Core's output
  - Create structured plans detailing step-by-step processes
  - Document tasks clearly in JSON format
  - Categorize tasks by type (planning, problem-solving, project, event)

### 3. Questioning Agent (Slot Filler)
- **Role**: Clarification and information augmentation
- **Responsibilities**:
  - Review and refine plans from the Planning Agent
  - Identify and fill any missing or ambiguous details
  - Generate clarifying questions
  - Calculate plan completeness scores

### 4. Orchestrator
- **Role**: Central coordinator
- **Responsibilities**:
  - Manage interactions between agents
  - Consolidate agent outputs into structured JSON
  - Generate final results ready for YAML conversion

## 🚀 Quick Start

### Environment Setup

Choose either **Conda** (recommended) or **venv**:

#### Option 1: Conda (Recommended)
```bash
# Create conda environment
conda env create -f environment.yml
conda activate albert-sandbox

# Verify installation
python --version
conda list
```

#### Option 2: Virtual Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup OpenAI API (Optional but Recommended)

```bash
# Manually set your API key
export OPENAI_API_KEY='your-api-key-here'

# For conda environments, you can also set it permanently:
conda env config vars set OPENAI_API_KEY=your-api-key-here
conda activate albert-sandbox  # Reactivate to load the variable
```

### Running the Demo

```bash
# Make sure your environment is activated
conda activate albert-sandbox  # or: source venv/bin/activate

# Run the main demo (requires OpenAI API key with billing)
python simple_demo.py

# Or run the fallback demo (works without OpenAI)
python demo_fallback.py
```

### Running Tests

```bash
# Run all tests
python -m unittest discover -s . -p "test_*.py" -v

# Run specific test file
python -m unittest test_albert_core.py -v

# Test with fallback agents
python demo_fallback.py
```

### Using the System Programmatically

```python
from orchestrator import Orchestrator

# Initialize the system
orchestrator = Orchestrator()

# Process a user request
result = orchestrator.process_user_request("I need help planning a project")

# Access the results
print(result['final_result']['summary'])
print(result['final_result']['action_plan'])
```

## 📊 JSON Output Structure

The system generates structured JSON output that follows these schemas:

### Albert Core Output
```json
{
  "agent_type": "albert_core",
  "user_input": "user request",
  "response": "initial response",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Planning Agent Output
```json
{
  "agent_type": "planning_agent",
  "plan_id": "plan_12345678",
  "tasks": [
    {
      "task_id": "task_12345678",
      "description": "task description",
      "priority": "high|medium|low",
      "status": "pending",
      "details": {
        "category": "planning|problem_solving|project|event|general",
        "estimated_time": "time estimate"
      }
    }
  ],
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Questioning Agent Output
```json
{
  "agent_type": "questioning_agent",
  "refined_plan": { /* enhanced plan */ },
  "questions": ["clarifying question 1", "question 2"],
  "missing_details": ["missing detail 1", "detail 2"],
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Final Orchestrator Output
```json
{
  "orchestrator_id": "orchestrator_12345678",
  "user_input": "original request",
  "albert_output": { /* Albert Core results */ },
  "planning_output": { /* Planning Agent results */ },
  "questioning_output": { /* Questioning Agent results */ },
  "final_result": {
    "summary": "executive summary",
    "action_plan": [
      {
        "action_id": "action_12345678",
        "type": "clarification|task_execution|detail_gathering",
        "description": "action description",
        "priority": "high|medium|low",
        "details": { /* action-specific details */ }
      }
    ],
    "recommendations": ["recommendation 1", "recommendation 2"]
  },
  "timestamp": "2024-01-01T10:00:00Z"
}
```

## 🔧 Technical Requirements

- **Language**: Python 3.x
- **Core Dependencies**: Python standard libraries + OpenAI API client
- **Optional**: OpenAI API key for intelligent agent behavior
- **Fallback**: Rule-based agents when OpenAI is not available
- **Output Format**: JSON (structured for future YAML conversion)
- **Testing**: unittest framework

## 🧪 Testing

The project follows test-driven development with comprehensive unit tests for each component:

- `test_albert_core.py`: Tests for user input processing and JSON output
- `test_planning_agent.py`: Tests for plan creation and task generation
- `test_questioning_agent.py`: Tests for plan refinement and question generation
- `test_orchestrator.py`: Tests for agent coordination and output consolidation

## 🚀 Development Workflow

1. **Initial Setup** ✅
   - [x] Define basic classes for each agent
   - [x] Establish JSON structure standard for agent outputs
   - [x] Develop initial orchestrator logic for agent communication

2. **Agent Logic Development** (Next Phase)
   - [ ] Enhance Albert Core with improved NLP capabilities
   - [ ] Expand Planning Agent with more sophisticated task planning
   - [ ] Improve Questioning Agent with advanced slot-filling logic
   - [ ] Conduct comprehensive unit testing

3. **Integration and Refinement** (Future)
   - [ ] Integrate all agents within the orchestrator framework
   - [ ] Perform system-wide testing and debugging
   - [ ] Validate JSON outputs adhere to project standards

4. **Evaluation and Documentation** (Future)
   - [ ] Conduct user-driven testing scenarios
   - [ ] Document each agent's logic, interactions, and JSON structure
   - [ ] Prepare final prototype demonstration

## 📝 Usage Examples

### Basic Planning Request
```python
request = "I need to organize a team meeting"
result = orchestrator.process_user_request(request)
# Generates tasks for meeting planning, identifies missing details like date/time/agenda
```

### Problem-Solving Request
```python
request = "Help me solve issues with our customer service response time"
result = orchestrator.process_user_request(request)
# Creates problem analysis tasks and asks clarifying questions about current metrics
```

### Project Creation Request
```python
request = "I want to build a mobile app for expense tracking"
result = orchestrator.process_user_request(request)
# Generates project tasks and identifies missing requirements and specifications
```

## 🔮 Future Extensions

- Enhanced NLP capabilities for Albert Core
- More sophisticated decision-making logic in the Planning Agent
- Robust information-gathering techniques for the Questioning Agent
- YAML output conversion functionality
- Web interface for interactive use
- Integration with external APIs and services

## 🤝 Contributing

This is a prototype project following the specifications in `instructions.md`. The system is designed to be modular and extensible for future enhancements.

## 📄 License

This project is a prototype developed according to the specifications in the instructions document. 