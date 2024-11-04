import os

def create_config():
    # Ensure config directory exists
    os.makedirs('config', exist_ok=True)

    # Configuration content
    agents_yaml_content = """
research_agent:
  temperature: 0.7
  max_tokens: 1000

food_agent:
  temperature: 0.7
  max_tokens: 1000

culture_agent:
  temperature: 0.7
  max_tokens: 1000

travel_agent:
  temperature: 0.7
  max_tokens: 1000

edit_agent:
  temperature: 0.7
  max_tokens: 1000
"""

    # Write agents.yaml file
    with open('config/agents.yaml', 'w') as f:
        f.write(agents_yaml_content)

if __name__ == "__main__":
    create_config()
    print("Configuration files created successfully!")