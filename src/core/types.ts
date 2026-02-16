/**
 * Core Types for Agent Registry
 */

export type HealthStatus = 'healthy' | 'unhealthy' | 'unknown';

export interface AgentMetadata {
  name?: string;
  version?: string;
  capabilities?: string[];
  tags?: Record<string, string>;
}

export interface RegisteredAgent {
  id: string;
  type: string;
  endpoint: string;
  metadata: AgentMetadata;
  registeredAt: number;
  lastHeartbeat: number;
  healthStatus: HealthStatus;
}

export interface DiscoveryOptions {
  type?: string;
  tags?: Record<string, string>;
  limit?: number;
}
