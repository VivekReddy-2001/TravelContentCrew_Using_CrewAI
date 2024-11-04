from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq

#from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
#tool = SerperDevTool()

from langchain_community.tools import DuckDuckGoSearchRun

tool = DuckDuckGoSearchRun()