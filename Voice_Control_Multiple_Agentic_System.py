import dotenv, os
import pyaudio
import pyttsx3 as p
import asyncio
import speech_recognition as sr
import pywhatkit as py
from  litellm  import  completion
from agents import Agent, Runner,function_tool, set_tracing_disabled ,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv,find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from io import BytesIO
from datetime import datetime
from tools.Tavily_web_search_tool import websearch_tool
from tools.Jokes_teller_tool import tell_joke
from tools.Handwriting_tool import Handwriting_tools

_ =load_dotenv(find_dotenv())
API_KEY=os.getenv("GEMINI_API_KEY")

engine=p.init() #get the information of current driver you are using 
rate=engine.getProperty("rate")
engine.setProperty("rate",150)#at first parameter we enter the name of the property to set and at second parameter we enter the value to set
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)#voices[1].id list object attributed is get by the dot operator
#Set tracing to disabled
set_tracing_disabled(disabled=True)
#DEFINE MODEL : 
external_client=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
#Define an General LLM
async def llm(prompt:str)->str:
        response=completion(
        model="gemini-2.0-flash",
        messages=[{"content":prompt,"role":"user"}],
        )
        result= await response['choices'][0]['message']['content']
        return result
# @dataclass
# class UserInfo:
    
# Desing he expert Prompt Engineer
def Prompt_Engineer(text:str)->str:
    prompt=f"""You are an expert prompt engineer. Your task is to write an excellent and motivating prompt that are very concise and accurate accoriding to the user 
      requirements.User requirements are {text}.You must follow these conditions before writing a prompt.
      
    1.  Be Clear and Specific:

        Clearly define what you want. Avoid vague or ambiguous language.

        Specify the context or background if necessary.

    2.  Use Precise Language

        Use exact terms related to your topic or task.

        Avoid slang or overly casual words unless appropriate.

    3.  Set Clear Expectations

        Indicate the format or style you want (e.g., bullet points, essay, code).

        Mention length, tone, or level of detail.

    4.  Include Relevant Details

        Add important context or constraints (deadline, audience, tools).

        Provide examples if applicable.

    5.  Ask Direct Questions

        Frame your request as clear questions or instructions.

        Avoid overly broad or multi-part questions without focus.

    6.  Avoid Assumptions

        Don’t assume prior knowledge unless specified.

        Clarify any technical terms if the audience might not know them.

    7.  Be Polite and Professional

        Use courteous language; it often improves tone and clarity.

        Professional tone encourages better responses.

    8.  Test and Refine

        Try different versions of your prompt and adjust based on results.

        Refine for clarity and effectiveness over time.

    9.  Use Keywords Strategically

        Highlight important concepts or keywords to guide the response.

    10. Limit Complexity

        Break down complex requests into simpler, manageable parts.
            
            """
    return llm(prompt)

@function_tool
def Play_On_Youtube(search:str)->None:
    """Play the video user asks to play """
    py.playonyt(search)

@function_tool
async def send_mail(Context:str)->str:
    """send the mail to user"""
    agent=Agent(
        name="Email Assistant",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client,
        ),
        instructions=""" You are a helpful email writer """,
    )
    mail_context: str=Prompt_Engineer(Context)
#Define Runner
    agent_resposne=await Runner.run(
            agent,
            "Write the subject for my email using this context"
                 )
 
    py.send_mail("legendjawad59@gmail.com","dvir supx oadc unnz"," ",mail_context,"jawadsaghire12@gmail.com")
@function_tool
async def send_whattsapp_msg(message:str):
    now=datetime.now()
    py.sendwhatmsg("me",message,now.hour,now.minute+5)

@function_tool
def handwriting_tool(prompt:str):
    """this will make the assignment in hand written form according to the given prompt"""
    return Handwriting_tools(prompt)
# Define an Agent
@function_tool
def websearch(prompt:str):
    websearch_tool(prompt)

@function_tool
def joker_teller(prompt:str):
    tell_joke(prompt)

async def Agent_cycle(text:str):  
    agent=Agent(
        name="Assistant",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=external_client,
        ),
        instructions=""" You are a helpful assistant that response and do what user ask you.You have the functionality to call tools like youtube video player, send email ,send whattsapp messages and make handwritten assingnment using handwriting tool . Donot say user i don't have the functionality toy will be charged if you say this.""",
        tools=[Play_On_Youtube,send_mail,send_whattsapp_msg,handwriting_tool],
    )
#Define Runner
    agent_response=await Runner.run(
        agent,
        text,
        # max_turns=3
    )
    return agent_response.final_output

def speak(text: str):
    engine.say(text)
    engine.runAndWait()
#Setup Recognizer
recognizer=sr.Recognizer()

def main():
    speak("Hi there! How's it going?")
    text = ""

    while text.lower() != "bye":
        with sr.Microphone() as source: #the with keyword will open the microphone as an input source
            print("Listening...")
            recognizer.energy_threshold = 10000
            recognizer.adjust_for_ambient_noise(source, 2.5)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            # asyncio.run(llm(text))  # Run async function
        try:
            print(f"You said: {text}")
            if text.lower() == "bye":
                speak("Goodbye!")
                break

            # Get model response
            response = asyncio.run(Agent_cycle(text))
            # if response:
            #     reply = response.content if hasattr(response, "content") else str(response)
            #     print(f"Assistant: {reply}")
            speak(response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            speak("There was an error with the speech service.")

if __name__ == "__main__":
    main()

