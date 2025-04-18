from langchain import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from llm import openai_llm



def generate_transcript_summary(call_transcript):

    summary_prompt = PromptTemplate(
        input_variable = ["call_transcript"],
        template = """
    
        You are an expert criminal intelligence analyst extracting structured insights from surveillance audio transcripts.

        Your goal is to summarize the content into a structured format based on the following schema:

        ### SCHEMA:
        - Acceptable Node Types:
            - Person (properties: name, alias, age, sex)
            - Operations (Drug Trafficking, Illegal Arms, Money Laundering, Upper Management)
            - Location (properties: name, location_type: [Warehouse, Meeting Spot])
            - Special Event (Only criminally organized events, e.g., Drop Night, Green Exchange)
            - Item (Illegal Arms, Controlled Substances, Stash of Cash)

        - Acceptable Relationship Types:
            - task (Person → Operation), its properties are (timestamp)
            - was_at (Person → Location),its properties are (timestamp, meeting_reason)
            - operates (Person → Operation)
            - task (Item → Person),its properties are (timestamp, description)

        ### Instructions:
            - Extract and summarize all nodes and relationships that are implicitly or explicitly mentioned in the transcript.
            - All events should include timestamps if mentioned or inferred.
            - Maintain natural ambiguity where needed, but still attach the correct schema label.
            - Use the Boss’s alias if mentioned (e.g., "Southpaw" or "Silver Ring").
            - Do NOT include irrelevant events, people, or objects.
            - Structure the summary as a list of identified nodes and relationships, with clarity and schema labels.

        ### Input Transcript:
        {transcript}

        ### Output (Example Structure):
            - Person: Sam (alias: "Ghost", age: 34, sex: "M")
            - Operation: Drug Trafficking
            - Location: North Warehouse (location_type: "Warehouse")
            - was_at: Sam → North Warehouse (timestamp: "2025-04-09T20:00", meeting_reason: "Delivery Oversight")
            - task: Sam → Drug Trafficking (timestamp: "2025-04-09T21:00")
            - task: Concealed SMGs → Sam (timestamp: "2025-04-09T21:10", description: "Hidden under crates")


        ### Important Information
            - Only generate the summary solely on the content of ###Input Transcript, do not infer the content based on the given examples
            (continue for all persons, locations, items, etc.)

    """
)


    summary_chain = (
        {"tone": RunnablePassthrough(), "summary_type": RunnablePassthrough(), "transcript": RunnablePassthrough()}
        | summary_prompt
        | openai_llm
    )
    response = summary_chain.invoke({"transcript": call_transcript})
    summary_content = response.content

    return summary_content

