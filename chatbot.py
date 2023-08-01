import openai
import uuid


class ChatGPTBot:
    def __init__(self, api_key, engine="davinci", data_file="prompts.txt"):
        self.api_key = api_key
        self.engine = engine
        self.data_file = data_file
        self.prompts = []
        self.load_prompts()
        self.initialize_gpt3()

    def initialize_gpt3(self):
        openai.api_key = self.api_key

    def load_prompts(self):
        try:
            with open(self.data_file, 'r') as file:
                for line in file:
                    unique_id, prompt = line.strip().split('|')
                    self.prompts.append({"id": unique_id, "prompt": prompt})
        except FileNotFoundError:
            self.prompts = []

    def save_prompts(self):
        with open(self.data_file, 'w') as file:
            for item in self.prompts:
                file.write(f"{item['id']}|{item['prompt']}\n")

    def create_prompt(self, prompt):
        unique_id = str(uuid.uuid4())
        self.prompts.append({"id": unique_id, "prompt": prompt})
        self.save_prompts()
        return unique_id

    def get_response(self, unique_id):
        for item in self.prompts:
            if item['id'] == unique_id:
                response = openai.Completion.create(
                    engine=self.engine,
                    prompt=item['prompt'],
                    max_tokens=100
                )
                return response['choices'][0]['text']
        return "Prompt not found."

    def update_prompt(self, unique_id, new_prompt):
        for item in self.prompts:
            if item['id'] == unique_id:
                item['prompt'] = new_prompt
                self.save_prompts()
                return True
        return False

    def delete_prompt(self, unique_id):
        for i, item in enumerate(self.prompts):
            if item['id'] == unique_id:
                del self.prompts[i]
                self.save_prompts()
                return True
        return False
