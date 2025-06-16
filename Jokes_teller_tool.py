import pyjokes 
def tell_joke(prompt:str):
    pyjokes.get_jokes()

if __name__=="__main__":
    tell_joke("Tell me a joke")