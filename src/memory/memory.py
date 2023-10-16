import tiktoken

class Memory:

    def __init__(self, initial_prompt=None, max_tokens=3000):
        if initial_prompt is None:
            initial_prompt = ""
        self.messages = [
            {
                "role": "system",
                "content": initial_prompt
            }
        ]
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def add(self, message):
        self.messages.append(dict(message))

    def delete_history(self):
        while True:
            total_tokens = 0
            for message in self.messages:
                if message["content"] != None:
                    message_tokens = len(self.encoding.encode(message["content"]))
                    total_tokens += message_tokens
            if total_tokens > self.max_tokens:
                self.messages[1:] = self.messages[2:]
            else:
                return

    def __str__(self):
        return "\n".join([str(message) for message in self.messages])