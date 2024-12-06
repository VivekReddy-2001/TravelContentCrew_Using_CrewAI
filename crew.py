#research agent, food enthusiast agent, culture specalist agent, travel planner agent, editior agent
from crewai import Agent, Crew, Process, Task
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
    Defining different agents,task, and crew to 
    create content for travel blog
    """
    def __init__(self, topic: str):
        """Initialize the crew with a specific topic"""
        #super().__init__()  # Add this line to properly initialize CrewBase
        self.topic = topic
        #self.llm=LLM(model="ollama/crewai-gemma2")
        self.llm=ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
        
    #research agent
    def research_agent(self)-> Agent:
        return Agent(
        role="Travel Researcher", 
        goal="Gather comprehensive details about {self.topic}, including key landmarks, historical significance, and geographical features.",
        backstory=("A world-traveled researcher with a passion for discovering unique aspects of every location, you specialize in uncovering the hidden stories of places like {self.topic}." 
        "With years of experience in geography and historical research, you provide detailed insights that bring {self.topic} to life for readers and travelers alike."),
        verbose=True,
        #llm=LLM(model="ollama/crewai-gemma2"),
        llm=self.llm,
        tools=[tool]
        )
     
    #food enthusiast agent
    def food_agent(self)->Agent:
        return Agent(
        role="Food Enthusiast",
        goal="Explore and describe the most popular dining spots, traditional dishes, and local food culture in {self.topic}.",
        backstory=("A food enthusiast with a passion for exploring the world's delicious cuisines, you specialize in offering practical advice and recommendations for those seeking to enjoy a diverse and delicious dining experience."
        "With years of experience in culinary research and cooking, you provide expert guidance that helps users tailor their meal plans to their individual tastes and dietary restrictions."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )
        
    #culture specialist agent
    def culture_agent(self)-> Agent:
        return  Agent(
        role="Culture Specialist",
        goal="Provide valuable insights into the customs, traditions, festivals, and social norms unique to {self.topic}.",
        backstory=("A culture enthusiast with a passion for understanding the world's rich heritage, you specialize in offering practical advice and recommendations for those seeking to learn more about their chosen location."
        "With years of experience in history and culture studies, you provide detailed insights that help users appreciate the unique aspects of {self.topic} and its rich past."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )

    #travel planner agent
    def travel_agent(self)-> Agent:
        return Agent(
        role="Travel Planner",
        goal="Offer practical travel advice for visiting {self.topic}, including the best times to visit, getting around, and ideal accommodation options.",
        backstory=("A seasoned travel planner with a reputation for curating seamless journeys, you excel at making travel to {self.topic} both accessible and enriching. From selecting the perfect accommodations to identifying easy transport options," 
        "your priority is to ensure that travelers’ experiences in {self.topic} are smooth, memorable, and well-organized."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )
    
    #editor agent
    def edit_agent(self)-> Agent:
        return Agent(
        role="Content Editor",
        goal="Review, organize, and polish the information gathered about {self.topic} into a cohesive, reader-friendly travel guide.",
        backstory=("An experienced editor with a background in travel writing," 
        "you’re known for transforming raw information into compelling stories." 
        "For {self.topic}, you bring together the insights from your team to craft an engaging and polished guide." 
        "Your mission is to create a seamless narrative that captures the essence of {self.topic} and provides value to every reader."),
        verbose=True,
        llm=self.llm,
        #tools=[document_writer]
        )
    #research task
    def research_location(self) -> Task:
        return Task(
            description=f"""Research comprehensive information about {self.topic}:
                1. Key landmarks and attractions in {self.topic}
                2. Historical background and significance of {self.topic}
                3. Geographical features and climate
                4. Transportation infrastructure
                5. General overview of {self.topic}
                
                Compile your findings in a detailed report that covers all these aspects.
                Focus on unique and lesser-known facts that would interest travelers visiting {self.topic}.
            """,
            expected_output=f"A comprehensive research report about {self.topic} including landmarks, history, geography, and infrastructure.",
            agent=self.research_agent()
        )
    #cuisine task
    def explore_cuisine(self) -> Task:
        return Task(
            description=f"""Investigate the food scene in {self.topic}:
                1. Traditional and popular local dishes of {self.topic}
                2. Must-visit restaurants and food markets
                3. Street food recommendations
                4. Local food customs and etiquette
                5. Special dietary considerations
                6. Best food neighborhoods
                7. Typical meal costs and budgeting tips
                
                Create a comprehensive food guide that includes practical tips for food lovers visiting {self.topic}.
            """,
            expected_output=f"A detailed food guide for {self.topic} covering local cuisine, restaurants, and dining customs.",
            agent=self.food_agent(),
            dependencies=[self.research_location()]
        )
    #culture task
    def analyze_culture(self) -> Task:
        return Task(
            description=f"""Analyze the cultural aspects of {self.topic}:
                1. Local customs and traditions
                2. Important festivals and celebrations
                3. Social norms and etiquette
                4. Religious and historical sites
                5. Arts and entertainment scene
                6. Local lifestyle and daily routines
                7. Cultural dos and don'ts
                
                Provide insights that will help travelers respect and appreciate local culture.
            """,
            expected_output=f"A cultural analysis report for {self.topic} covering traditions, customs, and social norms.",
            agent=self.culture_agent(),
            dependencies=[self.research_location()]
        )
    #travel task
    def create_travel_plan(self) -> Task:
        return Task(
            description=f"""Develop practical travel recommendations for {self.topic}:
                1. Best times to visit
                2. Recommended length of stay
                3. Accommodation options for different budgets
                4. Transportation tips
                5. Sample itineraries
                6. Safety considerations
                7. Budget planning
                8. Visa and entry requirements
                
                Create a practical guide that helps travelers plan their trip effectively.
            """,
            expected_output=f"A comprehensive travel plan for {self.topic} with practical recommendations and itineraries.",
            agent=self.travel_agent(),
            dependencies=[self.research_location(), self.analyze_culture()]
        )
    #final content 
    def edit_final_content(self) -> Task:
        return Task(
            description=f"""Review and compile all information about {self.topic} into a cohesive travel guide:
                1. Organize all collected information logically
                2. Ensure consistency in tone and style
                3. Add engaging transitions between sections
                4. Include practical tips and callout boxes
                5. Proofread for accuracy and clarity
                6. Format content for easy reading
                7. Add necessary citations and references
                
                Create a final, polished travel guide that's engaging and informative.
            """,
            expected_output=f"A polished, comprehensive travel guide for {self.topic} combining all research and recommendations.",
            agent=self.edit_agent(),
            dependencies=[
                self.research_location(),
                self.explore_cuisine(),
                self.analyze_culture(),
                self.create_travel_plan()
            ]
        )
    #function for running crew
    def run_crew(self):
        crew = Crew(
            agents=[
                self.research_agent(),
                self.food_agent(),
                self.culture_agent(),
                self.travel_agent(),
                self.edit_agent()
            ],
            tasks=[
                self.research_location(),
                self.explore_cuisine(),
                self.analyze_culture(),
                self.create_travel_plan(),
                self.edit_final_content()
            ],
            verbose=True
        )
        return crew.kickoff()

if __name__ == "__main__":
    travel_crew = TravelContentCrew(topic="Hyderabad")
    result = travel_crew.run_crew()
    print(result)