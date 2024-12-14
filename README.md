# 🌍 Make My Trip -- AI Travel Planning Assistant

## ✨ Overview

Make My Trip is an intelligent travel planning assistant designed to create comprehensive and efficient travel itineraries. Leveraging multiple AI agents, it helps you:

- Research destinations ✉️
- Find flight deals ✈️
- Explore local cuisines 🍔
- Generate optimized travel plans, including distances and route suggestions ▶️

This project is powered by the CrewAI framework and integrates Large Language Models (LLMs) for intelligent task delegation and execution.

---

## 🌍 Features

- **✨ Destination Research**: Gathers information about landmarks, transportation options, history, and geography.
- **✈️ Flight Finder**: Searches for the cheapest and most convenient flights.
- **🍔 Cuisine Explorer**: Provides insights into local food culture, popular dishes, and dining recommendations.
- **🗜️ Optimized Travel Planner**: Generates a travel plan with calculated distances and an optimized sequence of visits.

---

## 📚 Getting Started

### 🛠️ Prerequisites

- Python 3.10.0
- Required libraries from `requirements.txt`:
  - `streamlit`
  - `crewai`
  - `crewai[tools]`
  - `langchain`
  - `python-dotenv`
  - `ipykernel`
  - `langchain_community`
  - `pypdf`
  - `langchain-openai`
  - `agentops`

### 📒 Project Structure

- **`tripplannerapp.py`**: The web app for the project. Entry point where tasks are initialized and executed.
- **`tools.py`**: Contains additional tools to enhance agent capabilities.
- **`tripcrewai.py`**: Defines agents, tasks, and CrewAI processes.
- **`requirements.txt`**: Lists the required Python packages.

---

## ⭐ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Usage

To run the project, execute the following command:
```bash
python tripcrewai.py
```

---

## 🕵️‍♂️ Agents Overview

- **✨ Research Agent**: Collects extensive information about the specified location.
- **🍔 Food Agent**: Analyzes local cuisine and dining options.
- **✈️ Flight Agent**: Searches for flights and recommends the best options.
- **⏳ Travel Agent**: Creates an efficient travel plan for the destination.

---

## 🔖 Streamlit App

### **💡 Input**
- **Starting Point**: Starting location of your trip.
- **Destination**: Place you want to travel to.
- **Travel Dates**: Dates for your trip.
- **Number of Days**: Duration of your trip.

### **📊 Output**
- Generates an optimized travel itinerary with distance calculations and routes.
- Sample Output:

![Alt Text](https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI/blob/main/trip_planner_1.png)
![Alt Text](https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI/blob/main/trip_planner-2.png)
![Alt Text](https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI/blob/main/trip_planner_3.png)
![Alt Text](https://github.com/VivekReddy-2001/TravelContentCrew_Using_CrewAI/blob/main/trip_planner_4.png)

---


## 📢 Contact

For questions or feedback, feel free to reach out to :

**Vivek** at [vivekreddy3812@gmail.com](mailto:vivekreddy3812@gmail.com).
**Rahul** at [jangili.r@northeastern.edu](mailto:jangili.r@northeastern.edu).

---
