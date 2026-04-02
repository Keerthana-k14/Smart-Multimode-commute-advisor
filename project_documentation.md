# Smart Multimodal Commute Advisor
## Project Documentation - Phase 1

### 1. Abstract
The **Smart Multimodal Commute Advisor** is an AI-driven urban travel optimization platform. It addresses the growing challenge of urban congestion by providing real-time travel time predictions across various modes of transport—Bus, Metro, Cab, and Two-Wheeler. By integrating Machine Learning (ML) for predictive modeling and Explainable AI (XAI) for user transparency, the system empowers commuters to make informed, efficient travel decisions.

---

### 2. Problem Statement
Urban centers, particularly hubs like Bangalore, face escalating traffic congestion that significantly impacts travel time, air quality, and productivity. Existing navigation tools often focus on a single mode of transport (usually cars) or provide static public transport schedules. There is a critical need for a system that:
-   Compares **multiple transport modes** side-by-side.
-   Accounts for **real-time traffic congestion** levels.
-   Provides **human-readable rationales** (XAI) for its recommendations.

---

### 3. Project Objectives
-   **Predictive Accuracy**: Utilize historical traffic data to forecast commute durations with high precision.
-   **Multi-Modal Integration**: Support Bus, Metro, Two-Wheeler, and Cab commute options.
-   **Transparency through XAI**: Explain *why* a certain mode is recommended to build user trust.
-   **Interactive Experience**: Provide a dynamic map-based interface for easy route selection and result visualization.
-   **Data-Driven Improvement**: Implement a feedback mechanism to continuously refine the prediction models.

---

### 4. System Architecture

#### 4.1 Frontend (React.js)
The user interface is designed for speed and clarity.
-   **Mapping**: Uses Leaflet for interactive area and road selection.
-   **State Management**: React Hooks for handling user preferences and API responses.
-   **Responsiveness**: Modern CSS with a focus on usability during active travel.

#### 4.2 Backend (FastAPI)
A high-performance asynchronous API handles user requests.
-   **API Endpoints**: Facilitate route fetching, prediction serving, and feedback logging.
-   **CORS Support**: Configured for seamless communication with the web frontend.

#### 4.3 Machine Learning Layer
-   **Model**: Regressor models (Scikit-Learn) trained on historical Bangalore traffic data.
-   **Features**: Time of day, Day of week, Congestion level, and Road-specific metrics.
-   **XAI Engine**: A custom logic layer that analyzes the model outputs to generate human-readable explanations.

---

### 5. Data & Methodology

#### 5.1 Dataset
The project utilizes a specialized **Bangalore Traffic Dataset** (Kaggle-sourced), which includes detailed records of:
-   Area and Road networks.
-   Travel Time Index (TTI) across different time slots.
-   Historical congestion percentages.

#### 5.2 Analysis Pipeline (Notebooks)
1.  **Exploratory Data Analysis (EDA)**: Visualizing peak congestion hours and problematic road segments.
2.  **Preprocessing**: Handling missing values, encoding categorical variables (Area, Road), and feature scaling.
3.  **Model Training**: Comparing various regression algorithms to minimize Mean Absolute Error (MAE).
4.  **Evaluation**: Validating model performance against a test set to ensure reliability.

---

### 6. Key Features

-   **Intelligent Mode Switching**: Dynamically recommends Metro for high-congestion periods and cabs for off-peak hours.
-   **Real-time Traffic Simulation**: Simulates various congestion scenarios to show how commute times change.
-   **Explainable Recommendations**: e.g., "Two-wheeler is recommended as it bypasses the current 80% congestion on Outer Ring Road."
-   **User Feedback Collection**: Allows users to report actual trip times to help the model learn from real-world deviations.

---

### 7. Future Scope
-   **Phase 2: Real-time Integration**: Integrate live Google Maps/Traffic APIs for real-time data ingestion.
-   **Phase 3: Personalized Profiles**: Learn user preferences (e.g., preference for low cost vs. high speed).
-   **Phase 4: Multi-City Expansion**: Scale the model architecture to other metropolitan areas.

---

### 8. Conclusion
The Smart Multimodal Commute Advisor represents a significant step towards intelligent urban mobility. By combining predictive power with transparent reasoning, it offers a more nuanced and helpful tool for the modern commuter than traditional navigation apps.
