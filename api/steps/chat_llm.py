import os
from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser


llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.environ.get("OPEN_API_KEY"),
)


system_prompt = """
    You are a prompt analysis assistant. Your task is to review and evaluate the effectiveness of a given prompt. For each prompt provided, provide the following analysis:
    1. **Clarity**: Is the prompt clear and easy to understand? If not, suggest improvements.
    2. **Focus**: Does the prompt clearly define the task and scope? If there's ambiguity, point it out and suggest a clearer focus.
    3. **Context**: Does the prompt provide adequate background or context for the task? If more context is needed, specify what should be added.
    4. **Tone and Role**: Does the prompt set the correct tone and define the assistant's role appropriately? If the tone is inconsistent or the role isn't clear, provide suggestions.
    5. **Conciseness**: Is the prompt brief yet comprehensive? If the prompt is too long or vague, suggest ways to make it more concise while maintaining clarity.
    Provide a detailed report with examples of potential improvements for each section.
"""


def chat_llm() -> RunnableSequence:
    prompt = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(
                """
                Analyze the user query prompt:
              {parsed_response}
              """
            ),
        ]
    )

    return prompt | llm | StrOutputParser()
