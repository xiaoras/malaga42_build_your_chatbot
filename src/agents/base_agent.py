import json
import openai

class BaseAgent:

    def __init__(self, memory, knowledge_base, model="gpt-3.5-turbo", prices=[0.0015, 0.0020]):
        self.memory = memory
        self.knowledge_base = knowledge_base
        self.model = model
        self.prompt_cost = prices[0]
        self.completion_cost = prices[1]
        self.cost_list = []
        self.total_cost = 0
        self.conversation = []

    def reply(self, question):

        human_message = {
            "role": "user",
            "content": question
        }
        self.memory.add(human_message)

        answer = False
        while not answer:

            agent_message = self.generate_response()
            self.memory.add(agent_message)

            if agent_message.content is not None:
                answer = agent_message.content

            else:
                function_call = agent_message.function_call
                function_name = function_call.name
                kwargs = json.loads(function_call.arguments)

                print(f"[Agent calling function {function_name} with arguments {kwargs}]\n")

                if function_name == self.knowledge_base.function_name:
                    function_output = self.knowledge_base.search(**kwargs)

                else:
                    function_output = "WARNING: Function not found!"

                function_message = {
                    "role": "function",
                    "name": function_name,
                    "content": function_output
                }
                self.memory.add(function_message)

        self.conversation.append([question, answer])

        return answer

    def generate_response(self):

        self.memory.delete_history()

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.memory.messages,
            functions=[self.knowledge_base.function],
            temperature=0
        )

        self.calculate_cost(response.usage)

        agent_message = response.choices[0].message

        return agent_message

    def calculate_cost(self, usage):
        cost = (usage.prompt_tokens * self.prompt_cost + usage.completion_tokens * self.completion_cost) / 1000
        self.cost_list.append(cost)
        self.total_cost += cost