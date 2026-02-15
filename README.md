# Agent Registry

Central registry for agent management and discovery.

## Features

- **Agent Registration** - Register agents with metadata
- **Agent Discovery** - Find agents by capabilities
- **Status Tracking** - Monitor agent availability
- **Capability Matching** - Match agents to tasks

## Quick Start

```python
from agent_registry import AgentRegistry

reg = AgentRegistry()
reg.register(agent_id="a1", name="Agent 1", capabilities=["nlp"])
found = reg.find_by_capability("nlp")
```

## License

MIT
