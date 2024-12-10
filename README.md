# Make My Trip -- AI Travel Planning Assistant

## Overview

Make My Trip is a travel planning assistant designed to help users create comprehensive and efficient travel itineraries. It leverages multiple AI agents to research destinations, find flight deals, explore local cuisine, and generate optimized travel plans that include distances and route suggestions. This project is built using the CrewAI framework and integrates LLM (Large Language Models) for intelligent task delegation and execution.

## Features

-**Destination Research**: Gathers information about landmarks, transportation options, history, and geography.
-**Flight Finder**: Searches for the cheapest and most convenient flights.
-**Cuisine Explorer**: Provides insights into local food culture, popular dishes, and dining recommendations.
-**Optimized Travel Planner**: Generates a travel plan with calculated distances between locations and an optimized sequence of visits.


## Getting Started

### Prerequisites

- Python 3.10.0
- Required libraries from `requirements.txt`:
  - streamlit
  - crewai
  - crewai[tools]
  - langchain
  - python-dotenv
  - ipykernel
  - langchain_community
  - pypdf
  - langchain-openai
  - agentops

### Project Structure

**tripplannerapp.py**: web app for project. Entry point for the project where tasks are initialized and executed.

tools.py: Contains additional tools for enhancing agent capabilities.

**tripcrewai.py**: Defines agents, tasks, and crew processes.

requirements.txt: Lists the required Python packages.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To run the project, execute the following command:
```bash
python tripcrewai.py
```


### Agents Overview

- **Research Agent**: Collects extensive information about the specified location.
- **Food Agent**: Analyzes local cuisine and dining options.
- **Flight Agent**: Searches for different flights available to destination location and recommends best flight to take.
- **Travel Agent**: Create an efficient travel plan for destination.

### streamlit app

- **Input**: 
**Starting point**: Starting point of your trip
**Destination**: Place that you want to travel
**Travel dates**: Enter Dates that you want to travel
**No_of_days**: Enter No of days of your trip.

-- **Output**:
Here's the output of streamlit app: [Download the PDF](file:///C:/Users/vivek/Downloads/tripplannerapp_pic.pdf).


## Contact

For questions or feedback, please reach out to [Vivek](vivekreddy3812@gmail.com).

