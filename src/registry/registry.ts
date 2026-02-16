/**
 * Agent Registry - Service registration and discovery
 */

import { RegisteredAgent, AgentMetadata, DiscoveryOptions, HealthStatus } from '../core/types';

export class AgentRegistry {
  private agents: Map<string, RegisteredAgent> = new Map();
  private heartbeatInterval: number = 30000;
  private cleanupInterval: number = 60000;

  constructor(heartbeatInterval?: number) {
    this.heartbeatInterval = heartbeatInterval || 30000;
  }

  /**
   * Register an agent
   */
  register(
    id: string,
    type: string,
    endpoint: string,
    metadata: AgentMetadata = {}
  ): RegisteredAgent {
    const agent: RegisteredAgent = {
      id,
      type,
      endpoint,
      metadata,
      registeredAt: Date.now(),
      lastHeartbeat: Date.now(),
      healthStatus: 'healthy'
    };
    
    this.agents.set(id, agent);
    return agent;
  }

  /**
   * Unregister an agent
   */
  unregister(id: string): boolean {
    return this.agents.delete(id);
  }

  /**
   * Update heartbeat
   */
  heartbeat(id: string): boolean {
    const agent = this.agents.get(id);
    if (!agent) return false;
    
    agent.lastHeartbeat = Date.now();
    agent.healthStatus = 'healthy';
    return true;
  }

  /**
   * Discover agents
   */
  discover(options: DiscoveryOptions = {}): RegisteredAgent[] {
    let results = Array.from(this.agents.values());
    
    // Filter by type
    if (options.type) {
      results = results.filter(a => a.type === options.type);
    }
    
    // Filter by tags
    if (options.tags) {
      results = results.filter(a => {
        if (!a.metadata.tags) return false;
        for (const [key, value] of Object.entries(options.tags!)) {
          if (a.metadata.tags![key] !== value) return false;
        }
        return true;
      });
    }
    
    // Limit results
    if (options.limit) {
      results = results.slice(0, options.limit);
    }
    
    return results;
  }

  /**
   * Get agent by ID
   */
  get(id: string): RegisteredAgent | undefined {
    return this.agents.get(id);
  }

  /**
   * Get all agents
   */
  getAll(): RegisteredAgent[] {
    return Array.from(this.agents.values());
  }

  /**
   * Get healthy agents
   */
  getHealthy(): RegisteredAgent[] {
    return this.discover({ limit: 1 }).filter(a => a.healthStatus === 'healthy');
  }

  /**
   * Cleanup stale agents
   */
  cleanup(staleTimeout: number = 60000): number {
    const now = Date.now();
    let count = 0;
    
    for (const [id, agent] of this.agents) {
      if (now - agent.lastHeartbeat > staleTimeout) {
        agent.healthStatus = 'unhealthy';
        count++;
      }
    }
    
    return count;
  }

  /**
   * Get registry size
   */
  size(): number {
    return this.agents.size;
  }
}
