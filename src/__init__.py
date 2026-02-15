"""Agent Registry - Central registry for agent management and discovery."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class AgentType(Enum):
    NVIDIA_GPU = "nvidia"
    AWS_TRAINIUM = "trainium"
    GOOGLE_TPU = "tpu"
    CPU = "cpu"


class Protocol(Enum):
    MCP = "mcp"
    A2A = "a2a"
    CUSTOM = "custom"
    HTTP = "http"


class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"


@dataclass
class Agent:
    agent_id: str
    name: str
    agent_type: AgentType = AgentType.CPU
    capabilities: List[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"agent_id": self.agent_id, "name": self.name, "status": self.status.value, "capabilities": self.capabilities}


class AgentRegistry:
    """Central registry for agent management and discovery."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.capability_index: Dict[str, List[str]] = {}
    
    def register(self, agent_id: str, name: str, capabilities: List[str], agent_type: AgentType = AgentType.CPU, metadata: Dict[str, Any] = None) -> Agent:
        agent = Agent(agent_id=agent_id, name=name, capabilities=capabilities, agent_type=agent_type, metadata=metadata or {})
        self.agents[agent_id] = agent
        
        for cap in capabilities:
            if cap not in self.capability_index:
                self.capability_index[cap] = []
            if agent_id not in self.capability_index[cap]:
                self.capability_index[cap].append(agent_id)
        
        return agent
    
    def unregister(self, agent_id: str) -> bool:
        if agent_id not in self.agents:
            return False
        
        agent = self.agents.pop(agent_id)
        
        for cap in agent.capabilities:
            if cap in self.capability_index and agent_id in self.capability_index[cap]:
                self.capability_index[cap].remove(agent_id)
        
        return True
    
    def find_by_capability(self, capability: str) -> List[Agent]:
        agent_ids = self.capability_index.get(capability, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]
    
    def find_by_type(self, agent_type: AgentType) -> List[Agent]:
        return [a for a in self.agents.values() if a.agent_type == agent_type]
    
    def find_available(self) -> List[Agent]:
        return [a for a in self.agents.values() if a.status in (AgentStatus.IDLE, AgentStatus.ACTIVE)]
    
    def update_status(self, agent_id: str, status: AgentStatus) -> bool:
        agent = self.agents.get(agent_id)
        if agent:
            agent.status = status
            return True
        return False
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)
    
    def list_all(self) -> List[Agent]:
        return list(self.agents.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self.agents),
            "by_type": {t.value: len(self.find_by_type(t)) for t in AgentType},
            "by_status": {s.value: len([a for a in self.agents.values() if a.status == s]) for s in AgentStatus},
            "capabilities": list(self.capability_index.keys())
        }


__all__ = ["AgentRegistry", "Agent", "AgentStatus", "AgentType", "Protocol"]
