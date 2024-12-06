from crewai import Agent, Crew, Process, Task
from textwrap import dedent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain.llms import Ollama
from tools import tool
from langchain_openai import ChatOpenAI
from litellm import completion
from crewai import LLM
from dotenv import load_dotenv
load_dotenv(override=True)
import os


class TravelContentCrew():
    """
    Defining different agents,task, and crew to create a travel planning assistant.
    This assistant gathers flight options, transportation recommendations,
    hotel options, and plans visits to tourist attractions based on user preferences.
    """
    def __init__(self, from_location: str,to_location:str,travel_date:str):
        """Initialize the crew with a specific starting point and destination and travel date"""
        #super().__init__()  # Add this line to properly initialize CrewBase
        self.from_location = from_location
        self.to_location = to_location
        self.travel_date = travel_date
        #self.llm=LLM(model="ollama/crewai-gemma2")
        self.llm=ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
        
    #research agent
    def research_agent(self)-> Agent:
        return Agent(
        role="Travel Researcher", 
        goal="Gather comprehensive details about {self.to_location}, including key landmarks, historical significance, and geographical features.",
        backstory=("A world-traveled researcher with a passion for discovering unique aspects of every location, you specialize in uncovering the hidden stories of places like {self.to_location}." 
        "With years of experience in geography and historical research, you provide detailed insights that bring {self.to_location} to life for readers and travelers alike."),
        verbose=True,
        #llm=LLM(model="ollama/crewai-gemma2"),
        llm=self.llm,
        tools=[tool]
        )
    
    def flight_agent(self) -> Agent:
        return Agent(
            role="Flight Finder",
            goal=f"Search for the cheapest flights from {self.from_location} to {self.to_location} on {self.travel_date}.",
            backstory="You are an experienced travel booking assistant, skilled at finding the best deals for flights.",
            verbose=True,
            llm=self.llm,
            tools=[tool]
        )    
     
    #food enthusiast agent
    def food_agent(self)->Agent:
        return Agent(
        role="Food Enthusiast",
        goal="Explore and describe the most popular dining spots, traditional dishes, and local food culture in {self.to_location}.",
        backstory=("A food enthusiast with a passion for exploring the world's delicious cuisines, you specialize in offering practical advice and recommendations for those seeking to enjoy a diverse and delicious dining experience."
        "With years of experience in culinary research and cooking, you provide expert guidance that helps users tailor their meal plans to their individual tastes and dietary restrictions."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )
        

    #travel planner agent
    def travel_agent(self)-> Agent:
        return Agent(
        role="Travel Planner",
        goal="Offer practical travel advice for visiting {self.to_location}, including the best times to visit, getting around, and ideal accommodation options.",
        backstory=("A seasoned travel planner with a reputation for curating seamless journeys, you excel at making travel to {self.to_location} both accessible and enriching. From selecting the perfect accommodations to identifying easy transport options," 
        "your priority is to ensure that travelers’ experiences in {self.to_location} are smooth, memorable, and well-organized."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )
    

    #research task
    def research_location(self) -> Task:
        return Task(
            description=f"""Research comprehensive information about {self.to_location}:
                1. Key landmarks and attractions in {self.to_location}
                2. Historical background and significance of {self.to_location}
                3. Geographical features and climate
                4. Transportation infrastructure
                5. General overview of {self.to_location}
                
                Compile your findings in a detailed report that covers all these aspects.
                Focus on unique and lesser-known facts that would interest travelers visiting {self.to_location}.
            """,
            expected_output=f"A comprehensive research report about {self.to_location} including landmarks, history, geography, and infrastructure.",
            agent=self.research_agent()
        )
        
    def find_flights_task(self) -> Task:
        return Task(
            description=dedent(f"""
                Search for the cheapest flights from {self.from_location} to {self.to_location}.
                The report must include:
                1. Airlines offering flights
                2. Departure and arrival times
                3. Prices for economy class
                4. Booking links or references

                Provide the final result in a structured format with links to book.
            """),
            expected_output="A structured list of flight options with prices and booking links.",
            agent=self.flight_agent()
        )
    #cuisine task
    def explore_cuisine(self) -> Task:
        return Task(
            description=f"""Investigate the food scene in {self.to_location}:
                1. Traditional and popular local dishes of {self.to_location}
                2. Must-visit restaurants and food markets
                3. Street food recommendations
                4. Local food customs and etiquette
                5. Special dietary considerations
                6. Best food neighborhoods
                7. Typical meal costs and budgeting tips
                
                Create a comprehensive food guide that includes practical tips for food lovers visiting {self.to_location}.
            """,
            expected_output=f"A detailed food guide for {self.to_location} covering local cuisine, restaurants, and dining customs.",
            agent=self.food_agent(),
            dependencies=[self.research_location()]
        )
    #travel task
    def create_travel_plan(self) -> Task:
        return Task(
            description=f"""Develop practical travel recommendations for {self.to_location}:
                1. Best times to visit
                2. Recommended length of stay
                3. Accommodation options for different budgets
                4. Best flight deals (use Flight Finder results)
                5. Sample itineraries
                6. Safety considerations
                7. Budget planning
                8. Visa and entry requirements
                
                Combine all information into a single, user-friendly travel guide.
            """,
            expected_output="""A comprehensive travel plan for {self.to_location} with:
                - Best flight options with url links 
                - Food recommendations
                - Hotel and accommodation suggestions
                - Key activities and sample itineraries
            """ ,
            agent=self.travel_agent(),
            dependencies=[self.research_location(), self.find_flights_task(),self.explore_cuisine()]
        )

    #function for running crew
    def run_crew(self):
        crew = Crew(
            agents=[
                self.research_agent(),
                self.food_agent(),
                self.flight_agent(),
                self.travel_agent(),
            ],
            tasks=[
                self.research_location(),
                self.explore_cuisine(),
                self.find_flights_task(),
                self.create_travel_plan(),
            ],
            verbose=True
        )
        return crew.kickoff()

if __name__ == "__main__":
    from_location=input(dedent("""What is the Starting Point  of your trip? """))
    to_location=input(dedent("""What are the cities that you want to travel in your trip? """))
    travel_date=input(dedent("""What is the date range you are intereseted in traveling?"""))
    
    travel_crew = TravelContentCrew(from_location=from_location, to_location=to_location,travel_date=travel_date)
    result = travel_crew.run_crew()
    print(result)