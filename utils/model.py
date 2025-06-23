from litellm import completion
def llm(prompt:str)->str:
        response=completion(
        model="gemini/gemini-2.0-flash",
        messages=[{"content":prompt,"role":"user"}],
        )
        result=response['choices'][0]['message']['content']
        return result
if __name__=="__main__":
        print(llm("hello world how are you?"))