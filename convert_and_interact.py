import json

def convert_to_intent_json(input_path, output_path):
    # Load the JSON dataset with explicit UTF-8 encoding
    with open(input_path, 'r', encoding='utf-8') as f:
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
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(intent_data, f, indent=4)

    print("Conversion to intent.json complete!")

def interactive_cli():
    # Load the JSON dataset with explicit UTF-8 encoding
    with open('./data/csi.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a dictionary to map tags to country information
    country_data = {entry['tag']: entry for entry in data}

    # Helper function to display available countries
    def display_countries():
        print("Available countries:")
        for tag, info in country_data.items():
            print(f"- {info['geopoliticalarea']} (Tag: {tag})")

    # Helper function to handle interactions within a country context
    def handle_country_context(country_tag):
        country_info = country_data[country_tag]
        country_name = country_info['geopoliticalarea']

        print(f"\nYou selected {country_name}. You can ask about:")
        print("1. Travel and Transportation")
        print("2. Health")
        print("3. Local Laws and Special Circumstances")
        print("4. Safety and Security")
        print("5. Entry and Exit Requirements")
        print("Type 'exit' to exit this country context.")

        while True:
            user_input = input(f"\nAsk a question about {country_name} or type 'exit' to leave: ").strip().lower()

            if user_input == 'exit':
                print(f"Exiting the context of {country_name}.")
                break

            if "travel" in user_input:
                print(f"Travel and Transportation:\n{country_info.get('travel_transportation', 'No information available.')}")
            elif "health" in user_input:
                print(f"Health:\n{country_info.get('health', 'No information available.')}")
            elif "law" in user_input or "special" in user_input:
                print(f"Local Laws and Special Circumstances:\n{country_info.get('local_laws_and_special_circumstances', 'No information available.')}")
            elif "safety" in user_input or "security" in user_input:
                print(f"Safety and Security:\n{country_info.get('safety_and_security', 'No information available.')}")
            elif "entry" in user_input or "exit" in user_input:
                print(f"Entry and Exit Requirements:\n{country_info.get('entry_exit_requirements', 'No information available.')}")
            else:
                print("Sorry, I didn't understand that. Please ask about travel, health, laws, safety, or entry/exit.")

    while True:
        print("\nWelcome to the Travel Information Assistant!")
        display_countries()

        country_tag = input("\nEnter the tag of the country you want to know about or type 'quit' to exit: ").strip().upper()

        if country_tag == 'QUIT':
            print("Goodbye!")
            break

        if country_tag in country_data:
            handle_country_context(country_tag)
        else:
            print("Invalid country tag. Please try again.")

if __name__ == "__main__":
    # Convert the csi.json to intent.json first
    convert_to_intent_json('./data/csi.json', './data/intent.json')

    # Start the interactive CLI
    interactive_cli()
