import os
import json
from datetime import datetime
import openai
from typing import List, Dict


class JournalManager:
    def __init__(self, journal_dir: str = "journal_entries"):
        self.journal_dir = journal_dir
        if not os.path.exists(journal_dir):
            os.makedirs(journal_dir)

    def write_entry(self, entry: str) -> None:
        """Save a journal entry to a file."""
        timestamp = datetime.now()
        filename = f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        filepath = os.path.join(self.journal_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(entry)
        print(f"Entry saved successfully at {filepath}")

    def get_all_entries(self) -> List[Dict[str, str]]:
        """Read all journal entries and return them as a list."""
        entries = []
        for filename in sorted(os.listdir(self.journal_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.journal_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    date = datetime.strptime(filename.split('_')[0], '%Y-%m-%d')
                    entries.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'content': content
                    })
        return entries


class PersonalAssistant:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.journal_manager = JournalManager()

    def get_context(self) -> str:
        """Prepare journal entries as context."""
        entries = self.journal_manager.get_all_entries()
        context = "Here are my journal entries:\n\n"
        for entry in entries:
            context += f"Date: {entry['date']}\n{entry['content']}\n\n"
        return context

    def ask_question(self, question: str) -> str:
        """Ask ChatGPT a question with journal context."""
        context = self.get_context()
        prompt = f"""Given these journal entries as context about my life:

{context}

Question: {question}

Please provide a response based on the information from my journal entries."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that provides insights based on personal journal entries."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response: {str(e)}"


def main():
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Please set your OPENAI_API_KEY environment variable")
        return

    assistant = PersonalAssistant(api_key)
    journal_manager = assistant.journal_manager

    while True:
        print("\n1. Write journal entry")
        print("2. Ask question about your journal")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            print("\nWrite your journal entry (press Ctrl+D or Ctrl+Z when finished):")
            entry_lines = []
            try:
                while True:
                    line = input()
                    entry_lines.append(line)
            except EOFError:
                entry = '\n'.join(entry_lines)
                journal_manager.write_entry(entry)

        elif choice == '2':
            question = input("\nWhat would you like to ask about your journal? ")
            response = assistant.ask_question(question)
            print("\nResponse:", response)

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()