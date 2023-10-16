import os
import re
import json

class KnowledgeBase:

    def __init__(self, vdb, max_chunks=3):
        self.vdb = vdb
        self.max_chunks = max_chunks
        self.function_name = "search_documentation"
        self.function = json.loads(self.search.__doc__)

    def search(self, query):
        """
        {
            "name": "search_documentation",
            "description": "Access information from internal documentation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's query."
                    }
                },
                "required": ["query"]
            }
        }
        """
        retrieved = self.vdb.similarity_search(query, k=self.max_chunks)
        context = {}
        for i, doc in enumerate(retrieved):
            file_path = doc.metadata["source"]
            file_name = os.path.normpath(file_path).split(os.sep)[-1]
            title = f"INFORMATION {i + 1} (from {file_name})"
            content = re.sub("\s+", " ", doc.page_content)
            context[title] = content
        return str(context)