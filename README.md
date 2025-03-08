# Tourist Guide Web Application

## Overview
This project is a simple Flask-based web application that acts as a guide to tourist attractions in Beijing and Shanghai. The app includes:

- A homepage with buttons linking to different attraction-themed landing pages.
- Each landing page provides information about a specific attraction (e.g., the Forbidden City, Tian'anmen Square) and includes the current weather conditions at that location.
- The site also displays forecasts for the attractions' weather.

## Core Features

### Homepage
- A list of tourist attractions (such as the Forbidden City, Tian'anmen Square).
- Each attraction links to its own landing page.

### Attraction Pages
Each attraction has its own page with:
- Pictures of the attraction.
- Information and descriptions about the attraction.
- Weather conditions (current weather and forecasts) for that attraction, fetched from an API like OpenWeatherMap.

### Weather API Integration
- Use a weather API to dynamically display weather data for each attraction.
- Fetch data using Python (via Flask) and display it on the attraction pages.

## Possible Future Goals
- Publicly accessible website (hosted on a domain) with user interaction, data collection, and analytics (not focused on this part yet).

## Tech Stack
- **Python**: Backend for running Flask and fetching weather data.
- **HTML/CSS**: Frontend for designing the homepage and landing pages.
- **Flask**: Web framework to serve the pages and handle routes for different attractions.
- **Weather API (e.g., OpenWeatherMap)**: To fetch weather information.
- **JSON**: For storing information about the attractions (titles, descriptions, images).

## Folder Structure

## Summary
The goal is to have a homepage with links to individual attraction pages, where you display attraction-specific details and dynamic weather information. Initially, the focus is on running the app locally, with potential future plans to make it public and integrate analytics.