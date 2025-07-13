# AI Agent Sandbox

A multi-agent system that orchestrates AI-powered agents for intelligent task planning and execution. 


## System Architecture

```
User Input → Albert Core → Planning Agent → Questioning Agent → Orchestrator → Results
                ↓              ↓              ↓              ↓
           AI/Fallback    AI/Fallback    AI/Fallback    Coordination
```

### Core Agents
- **Albert Core**: User interface and input processing
- **Planning Agent**: Strategic task generation and breakdown  
- **Questioning Agent**: Plan refinement and gap identification
- **Orchestrator**: Central coordination and result consolidation


## Project Structure

```
albert/
├── Core Agents
│   ├── albert_core.py          # Main user interface agent
│   ├── planning_agent.py       # Task planning and breakdown
│   ├── questioning_agent.py    # Plan refinement and validation
│   └── orchestrator.py         # Central coordination
├── Infrastructure  
│   ├── config.py              # Configuration management
│   ├── openai_utils.py        # AI API utilities
│   ├── json_schemas.py        # Data structure standards
│   └── logger_config.py       # Logging system
├── Demo
│   └── demo.py                # Main demonstration
└── Setup
    ├── requirements.txt       # Python dependencies
    └── environment.yml        # Conda environment
```
