import dotenv, os, asyncio, pyaudio
import pyttsx3 as p

import speech_recognition as sr
import pywhatkit as py
from  litellm  import  completion
from agents import Agent, Runner,function_tool, set_tracing_disabled ,OpenAIChatCompletionsModel, ItemHelpers, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv,find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from io import BytesIO
from datetime import datetime
from tools.Tavily_web_search_tool import websearch_tool
from tools.Jokes_teller_tool import tell_joke
from tools.Handwriting_tool import Handwriting_tools
from tools.Image_Generation_tool import image_generation
from utils.model import llm
from utils.prompt_engineer import Prompt_Engineer

enable_verbose_stdout_logging()
from together import Together
from dotenv import load_dotenv,find_dotenv
import asyncio
import os
from tavily import TavilyClient
from dotenv import load_dotenv,find_dotenv
from together import Together
import requests


_ =load_dotenv(find_dotenv())
API_KEY=os.getenv("GEMINI_API_KEY")
_=load_dotenv(find_dotenv())
key=os.getenv("TOGETHER_API_KEY")
client = Together(api_key=key)  # Replace with your actual API key

_ =load_dotenv(find_dotenv())
API_KEY=os.getenv("GEMINI_API_KEY")

engine=p.init() #get the information of current driver you are using 
rate=engine.getProperty("rate")
engine.setProperty("rate",170)#at first parameter we enter the name of the property to set and at second parameter we enter the value to set
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)#voices[1].id list object attributed is get by the dot operator
#Set tracing to disabled
set_tracing_disabled(disabled=True)
#DEFINE MODEL : 
external_client=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
    

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
def websearch(queries:str):
    """ This tool will search on the web and get the realtime information from the internet"""
    tavily_api_key=os.getenv("TAVILY_API_KEY")
    tavily_client=TavilyClient(api_key=tavily_api_key)
    response=tavily_client.search(query=queries,
                                search_depth="advanced",
                                include_raw_content="markdown",
                                max_results=1,
                                include_answer="advanced",
                                country="pakistan"
                                )
    # response=tavily_client.crawl(
    #     categories=["Contact"]
    # )
    return (response)

@function_tool
def joker_teller(prompt:str):
    """The function of this tool is to tell the jokes"""
    return tell_joke(prompt)

@function_tool
def image_generation(prompts:str):
    response = client.images.generate(
        prompt=prompts,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1200,
        height=1792,
        steps=2,
        n=2
    )
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    with open("image.jpg", "wb") as f:
        f.write(img_data)
    print("✅ Image is saved Successfully'")
    return f"image is created"
# prompts="Create an 8K resolution (8000 x 8000 pixels) ultra-high-definition picture of an anthropomorphic Charizard character. The character should pose confidently, featuring exaggerated feminine traits including a prominent bust, while maintaining classic Charizard attributes such as fiery wings, vivid orange scales, and a flaming tail. Dress the Charizard in a stylish, colorful bikini that harmonizes with the fiery orange and red color scheme. The background is a sunny beach scene with sparkling blue water and a clear sky, evoking a relaxed, summery atmosphere. The art style should blend realism and fantasy, with smooth shading, dynamic and cinematic lighting, and careful anatomical proportions to ensure the design is appealing and tasteful. Employ advanced digital painting techniques such as layering, blending, and detailed texturing to enhance realism and vibrancy. Use natural shadows and highlights to emphasize depth and form. Compose the image using principles of visual harmony, such as the golden ratio, for balanced and aesthetically pleasing composition."
# image_generation(prompts)


General_agent=Agent(
    name="Assistant",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    ),
    instructions=""" You are a helpful assistant that response and do what user ask you.You have the functionality to call tools like generate images,youtube video player, send email ,send whattsapp messages,web search tool for real time data and make handwritten assingnment using handwriting tool .You have the functionality to generate an image. Donot say user i don't have the functionality toy will be charged if you say this.""",
    tools=[Play_On_Youtube,send_mail,send_whattsapp_msg,handwriting_tool,websearch],
)

Image_Generation_Agent=Agent(
    name="Image generation Specialist",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    ),
    instructions=""" You are a helpful image generater. You have the functionality to generate an 8k image""",
    tools=[image_generation],
)
async def Agent_cycle(text:str):
    Manager=Agent(
        name="Manager",
         model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,),
        instructions="you are the manager of the AI team. Your task is to delegate task to specialized agent.",
        handoffs=[Image_Generation_Agent,General_agent]
    )
#Define Runner
    agent_response=await Runner.run(
        Manager,
        input=text,
        # max_turns=3
    )
    print("Agent Started")
    return agent_response.final_output
    # async for event in agent_response.stream_events():
    #             if event.type=="raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
    #                 return event.data.delta
        # if event.type=="raw_response_event" :
        #         continue
        # elif event.type=="agent_updated_stream_event":
        #     print(f"Agent updated: {event.new_agent.name}")
        #     continue
        # #when items are generated print them
        # elif event.type=="run_item_stream_event":
        #     if event.item.type=="tool_call_item":
        #         return "Calling Tool "
        #     elif event.item.type=="tool_call_output_item":
        #         return f"{event.item.output}"
        #     elif event.item.type=="message_output_item":
        #         return f"{ItemHelpers.text_message_output(event.item)}"
        #     else:
                # pass

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

#Setup Recognizer
recognizer=sr.Recognizer()

def main():
    speak("Hi")
    text = ""
    
    while text.lower() != "bye":
        try:
            with sr.Microphone() as source: #the with keyword will open the microphone as an input source
                print("Listening...")
                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 2.5)
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                # asyncio.run(llm(text))  # Run async function
                print(f"You said: {text}")
                if text.lower() == "bye":
                    speak("Goodbye!")
                    break

            # Get model response
                response = llm(text)
                if response:
                    reply = response.content if hasattr(response, "content") else str(response)
                    print(f"Assistant: {reply}")
                speak(response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            speak("There was an error with the speech service.")

if __name__ == "__main__":
    main()

