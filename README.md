# BramHacks-2025
BramHacks 2025 project developed by space-loving students.

⭐ [WebApp Prototype and Information](https://projectpontus.netlify.app)

## Description
Project PONTUS (Plastic Observation and Navigation Tracking Using Satellites) is an initiative aimed at addressing the growing concern of microplastic pollution in our oceans. By leveraging NASA's CYGNSS OSCARand satellite data and advanced mathematical modelling techniques, we seek to track and predict the movement of microplastics, providing valuable insights for environmental conservation efforts.

The project consists of three main components: a predictive model that simulates the transport of microplastics based on oceanographic data, an interactive web-based map that visualizes the distribution and movement of these pollutants over time, and Scrappy, a robotic system designed to validate the presence of microplastic samples in targeted ocean regions to enhance the accuracy of our predictions and support large-scale cleanup operations.

## Technologies Used
Model and Web Application:
- NASA's CYGNSS OSCARand satellite data for oceanographic information
- Python, mathematical modelling techniques for prediction
- SvelteKit for building the web application
- MapLibre GL JS for interactive map visualization

Robotic System (Scrappy):
- ESP32 microcontroller for control and communication
- Onboard camera for sample collection validation
- Remote operation (steering and grappling) paired with the web application
- LEDs to support underwater operation
- YOLOv8 computer vision model for microplastic detection

## Acknowledgements
Thank you to BramHacks for hosting the hackathon and providing us an opportunity to explore our passion for space. A special thanks to Make Stuff Move, who provided complimentary access to their robotics components, allowing us to bring Scrappy to life in one day. 