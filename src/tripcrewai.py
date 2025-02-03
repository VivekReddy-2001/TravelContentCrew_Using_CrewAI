from crewai import Agent, Crew, Process, Task
from textwrap import dedent
from crewai.project import CrewBase, agent, crew, task
#from crewai_tools import SerperDevTool
#from langchain.llms import Ollama
from tools import tool
from langchain_openai import ChatOpenAI
from litellm import completion
from crewai import LLM
from dotenv import load_dotenv
load_dotenv(override=True)
import os
import agentops
from IPython.display import display
from PIL import Image
# agentops.init(os.getenv("AGENT_OPS_API_KEY"))
# from recommendations import recommendations
import glob
import matplotlib.pyplot as plt

class TravelContentCrew():
    """
    Defining different agents,task, and crew to create a travel planning assistant.
    This assistant gathers flight options, transportation recommendations,
    hotel options, and plans visits to tourist attractions based on user preferences.
    """
    def __init__(self, from_location: str,to_location:str,travel_date:str,no_of_days:int):
        """Initialize the crew with a specific starting point and destination and travel date"""
        self.from_location = from_location
        self.to_location = to_location
        self.travel_date = travel_date
        self.no_of_days= no_of_days
        #self.llm=LLM(model="ollama/crewai-gemma2")
        self.llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))
        
    #research agent
    def research_agent(self)-> Agent:
        return Agent(
        role="Travel Researcher", 
        goal="Gather comprehensive details about {self.to_location}, including different types of transporation from {self.from_location} are available,key landmarks, historical significance, and geographical features.",
        backstory=("A world-traveled researcher with a passion for discovering unique aspects of every location, you specialize in uncovering the hidden stories of places like {self.to_location}." 
        "With years of experience in geography and historical research, you provide detailed insights that bring {self.to_location} to life for readers and travelers alike."),
        verbose=True,
        #llm=LLM(model="ollama/crewai-gemma2"),
        llm=self.llm,
        tools=[tool]
        )
    #flight agent
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
    #Trip Planning agent
    def travel_agent(self) -> Agent:
        return Agent(
        role="Optimized Travel Planner",
        goal=f"""Create an efficient travel plan for {self.to_location} for {self.no_of_days} days that includes:
            - Best routes between locations
            - Distances between each location
            - Recommended sequence of visits to minimize travel time
            - Incorporate insights from research, flight details, and food recommendations
        """,
        backstory=("A travel optimization expert, you excel in designing itineraries that are both enjoyable and efficient. Your plans save time and make travel smooth."),
        verbose=True,
        llm=self.llm,
        tools=[tool]
        )


    #research task
    def research_location(self) -> Task:
        return Task(
            description=f"""Research comprehensive information about {self.to_location}:
                1. Key landmarks and attractions in {self.to_location}
                2. Different types of of transportation available from {self.from_location} to {self.to_location}
                3. Historical background and significance of {self.to_location}
                4. Geographical features and climate
                5. Transportation infrastructure
                6. General overview of {self.to_location}
                
                Compile your findings in a detailed report that covers all these aspects.
                Focus on unique and lesser-known facts that would interest travelers visiting {self.to_location}.
            """,
            expected_output=f"A comprehensive research report about {self.to_location} including landmarks, transportation, history, geography, and infrastructure.",
            agent=self.research_agent()
        )
    #flight task  
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
    #Travel Plan Task
    def create_travel_plan(self) -> Task:
        return Task(
        description=f"""Using the results from previous tasks, create a comprehensive travel plan for {self.to_location}  for {self.no_of_days}:
            1. Use flight details from find_flights_task.
            2. Different ways of transportation available from {self.from_location} to {self.to_location} and average cost for each type
            3. Include food recommendations from explore_cuisine.
            4. Incorporate information from research_location and calculate distances between locations and optimize the sequence of visits.
            5. Best times to visit
            6. Visa and entry requirements
        """,
        #5. Calculate distances between suggested activities and plan accordingly.
        expected_output="""A comprehensive travel plan for {self.to_location} with:
            - Best flight options
            - Different Transportation Options
            - Food recommendations
            - Hotel suggestions 
            - Key activities and itineraries with practical travel advice and show the distance between each location as well.
        """,
        agent=self.travel_agent(),
        dependencies=[self.research_location(), self.find_flights_task(), self.explore_cuisine()]
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
    
    import os



    def show_images_grid(self, city_folder):
        city_names = [city for city in os.listdir(city_folder) if os.path.isdir(os.path.join(city_folder, city))]
        
        for city in city_names:
            city_path = os.path.join(city_folder, city)
            image_files = [img for img in os.listdir(city_path) if img.endswith(".jpg")]
            
            if image_files:
                print(f"Displaying images for {city}:")

                # Prepare grid
                n = len(image_files)
                cols = 3  # Set the number of columns in the grid
                rows = (n // cols) + (n % cols > 0)  # Calculate the number of rows
                
                # Create subplots
                fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
                axes = axes.flatten()  # Flatten to make indexing easier

                for i, img_file in enumerate(image_files):
                    img_path = os.path.join(city_path, img_file)
                    try:
                        img = Image.open(img_path)
                        axes[i].imshow(img)
                        axes[i].axis('off')  # Hide axes
                        axes[i].set_title(img_file)
                    except Exception as e:
                        print(f"Error displaying image {img_file}: {e}")

                # Hide any extra axes if the number of images is less than grid size
                for i in range(n, len(axes)):
                    axes[i].axis('off')

                plt.tight_layout()
                plt.show()
            else:
                print(f"No images found for {city}.")

# Example usage



        

if __name__ == "__main__":
    from_location=input(dedent("""What is the Starting Point  of your trip? """))
    to_location=input(dedent("""What are the cities that you want to travel in your trip? """))
    travel_date=input(dedent("""What is the date range you are intereseted in traveling?"""))
    no_of_days=input(dedent("""Number of days to travel in your trip"""))
    
    travel_crew = TravelContentCrew(from_location=from_location, to_location=to_location,travel_date=travel_date, no_of_days=no_of_days)
    
    travel_crew.show_images_grid('D:/make_my_trip/TravelContentCrew_Using_CrewAI/src/City_Photos')
  
    # print(result)
    

