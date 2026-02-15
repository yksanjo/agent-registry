#!/usr/bin/env python3
"""Demo for Agent Registry."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import AgentRegistry, AgentType

def main():
    print("Agent Registry Demo")
    reg = AgentRegistry()
    reg.register("a1", "Agent 1", ["nlp", "vision"])
    reg.register("a2", "Agent 2", ["nlp"])
    found = reg.find_by_capability("nlp")
    print(f"Found {len(found)} agents with nlp capability")
    print("Done!")

if __name__ == "__main__": main()
