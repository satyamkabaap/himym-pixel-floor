import os
import json

def load_persona(agent_name):
    with open(f"agents/{agent_name}/persona.md", "r") as f:
        return f.read()

def get_world_state():
    with open("world_state.json", "r") as f:
        return json.load(f)

# Placeholder for agent logic
if __name__ == "__main__":
    import sys
    agent_name = sys.argv[1]
    persona = load_persona(agent_name)
    print(f"I am {agent_name}. My persona: {persona[:50]}...")
