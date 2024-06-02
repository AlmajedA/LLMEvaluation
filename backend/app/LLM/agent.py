from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
import markdown


class Agent:
    def __init__(self, tools):
        self.tools = tools
        
        # The Brain
        llm = ChatOpenAI(
            temperature=0.2,
            streaming=True,
            api_key="sk-proj-6soye3S7Rx9LcKyeop1HT3BlbkFJBYnHI0jVy6rrsbpZrEJC",
            callbacks=[StreamingStdOutCallbackHandler()],
            model="gpt-3.5-turbo" # try gpt-4 if available
        )

        # The Intent
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You are a specialized bot employed by the UAE Government to answer \
                questions and provide information from the Information and Services system. Follow these rules:
                - REPLY IN TEXT ONLY. DO NOT USE MARKDOWN OR HTML FORMATS.
                - USE ONLY THE DOCUMENT PROVIDED TO YOU.
                - IF YOU DO NOT KNOW THE ANSWER, ASK THE USER TO REPHRASE THE QUESTION.

                Your responses should be brief, helpful, and concise."""),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def ask(self, query):
        try:
            result = self.agent_executor.invoke({"input": query})['output']
            result = markdown.markdown(result)
            
            # Remove surrounding <p> tags if present
            if result.startswith('<p>'):
                result = result[3:-4]
            
            return result
        
        except Exception as e:
            return f"AgentError: {str(e)}"
