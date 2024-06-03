from langchain.llms import Replicate
from langchain.chains import LLMChain
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.prompts import ChatPromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import os
import markdown

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class AgentFalcon:
    def __init__(self, tools):
        # Initialize the LLM with specific parameters
        self.llm = Replicate(
            model="joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173",
            model_kwargs={"temperature": 1, "max_length": 256, "top_p": 1}
        )

        # Create a prompt template using ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a specialized bot employed by the UAE Government to answer \
            questions and provide information from the Information and Services system. Follow these rules:
            - REPLY IN TEXT ONLY. DO NOT USE MARKDOWN OR HTML FORMATS.
            - USE ONLY THE DOCUMENT PROVIDED TO YOU.
            - IF YOU DO NOT KNOW THE ANSWER, ASK THE USER TO REPHRASE THE QUESTION.
             
            Your responses should be brief, helpful, and concise.
            """),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # Initialize conversational memory
        conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )

        # Initialize the agent
        self.agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=self.llm,
            verbose=True,
            max_iterations=1,
            early_stopping_method='generate',
            memory=conversational_memory,
            handle_parsing_errors=True

        )

        # Assign the prompt to the agent's LLM (assuming agent's structure allows it)
        self.agent.agent.llm_chain.prompt = prompt


    def ask(self, query):
        try:
            # Execute the agent with the given query and get the result
            result = self.agent.invoke({"input": query})['output']
            return result
        except Exception as e:
            # Find the starting position of the LLM output
            start_pos = str(e).find("LLM output: ` ")

            # Extract the LLM output
            if start_pos != -1:
                llm_output = str(e)[start_pos+len("LLM output: ` "):]  # +1 to remove the leading `
                llm_output = llm_output.strip("` ")  # Remove leading and trailing backticks and spaces
            else:
                llm_output = ""
            return str(e)

# The rest of the Django views and configurations remains unchanged.
