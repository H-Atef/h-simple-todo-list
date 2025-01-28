
import asyncio
from groq import AsyncGroq
import importlib


module1 = 't_list.helper.ai_model_auth'

class GroqAIHashtagsGenerator:
    def __init__(self):
        self.groq_client = AsyncGroq(api_key=importlib.import_module(module1).API_KEY)


    async def get_hashtags(self, todo_task_title:str) -> list:
        
        try:
            # Make API request 
            chat_completion =  await self.groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"""
                        return only top 3 appropriate hashtags for this task {todo_task_title}
                        without any explaination
                       
                    """
                }],
                model="llama3-8b-8192",  # Assuming Groq uses Llama3 model
            )

            # Parse the result from the API
            predictions = chat_completion.choices[0].message.content

            # Return the result 
            return predictions.split()

        except Exception as e:
                return {}

