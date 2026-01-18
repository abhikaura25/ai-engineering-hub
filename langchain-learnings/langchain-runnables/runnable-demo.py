import random

class NakliLLM:
    def __init__(self):
        print('LLM Created ...')
    
    def predict(self, prompt):
        response_list = [
            'Delhi is capital of India',
            'IPL is a cricket league',
            "AI stand for artifical intelligence"
        ]
        return { 'response' : random.choice(response_list) }
    
class NakliPromptTemplate:
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables
    
    def format(self, input_dict):
        return self.template.format(**input_dict)
    
class NakliLLMChain:
    def __init__(self, prompt, llm):
        self.prompt = prompt
        self.llm = llm
    
    def run(self, input_dict):
        final_prompt = self.prompt.format(input_dict)
        result = self.llm.predict(final_prompt)
        return result['response']



template = NakliPromptTemplate(
    template="write poem about {topic}",
    input_variables=["topic"]
)

llm = NakliLLM()

chain = NakliLLMChain(prompt=template, llm=llm)

result = chain.run({"topic": "India"})

print(result)

    