import json

# Load the JSON dataset with explicit UTF-8 encoding
with open('./data/csi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize the structure for intent.json
intents = []

# Helper function to create patterns and responses
def create_intent(tag, patterns, responses):
    return {
        "tag": tag,
        "patterns": patterns,
        "responses": responses
    }

# Iterate through the dataset and extract intents and examples
for entry in data:
    tag = entry['tag']
    geopolitical_area = entry.get('geopoliticalarea', '')
    travel_transportation = entry.get('travel_transportation', '')
    health = entry.get('health', '')
    local_laws_and_special_circumstances = entry.get('local_laws_and_special_circumstances', '')
    safety_and_security = entry.get('safety_and_security', '')
    entry_exit_requirements = entry.get('entry_exit_requirements', '')

    if geopolitical_area:
        intents.append(create_intent(
            f"{tag}_geopolitical_area",
            [f"Tell me about {geopolitical_area}", f"Where is {geopolitical_area} located?", f"Information about {geopolitical_area}"],
            [geopolitical_area]
        ))

    if travel_transportation:
        intents.append(create_intent(
            f"{tag}_travel_transportation",
            ["How can I travel there?", "Tell me about transportation options", "What should I know about driving there?"],
            [travel_transportation]
        ))

    if health:
        intents.append(create_intent(
            f"{tag}_health",
            ["Tell me about the health services", "What medical facilities are available?", "Health information about the area"],
            [health]
        ))

    if local_laws_and_special_circumstances:
        intents.append(create_intent(
            f"{tag}_local_laws",
            ["What are the local laws?", "Tell me about the legal system", "Are there any special laws I should know?"],
            [local_laws_and_special_circumstances]
        ))

    if safety_and_security:
        intents.append(create_intent(
            f"{tag}_safety_security",
            ["Is it safe to travel there?", "What are the safety concerns?", "Tell me about security measures"],
            [safety_and_security]
        ))

    if entry_exit_requirements:
        intents.append(create_intent(
            f"{tag}_entry_exit",
            ["What are the entry requirements?", "Do I need a visa?", "Tell me about exit requirements"],
            [entry_exit_requirements]
        ))

# Create the final intent.json structure
intent_data = {"intents": intents}

# Save to intent.json
output_file_path = './data/intent.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(intent_data, f, indent=4)

print("Conversion to intent.json complete!")
