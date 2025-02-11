import json

CONFIG_FILE = "configuration.json"

# Load existing config
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Save updated config
def save_config(new_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(new_data, f, indent=4)

# Load data on import
config = load_config()

# Expose variables
chatbot_name = config["chatbot_name"]
Subtitle = config["Subtitle"]
Prompt = config["Prompt"]
