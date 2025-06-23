from .model import llm

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

if __name__=="__main__":
    print(Prompt_Engineer("make an beautiful image of a horse"))