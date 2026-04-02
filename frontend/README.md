# 💻 Smart Commute Advisor - Frontend

The frontend for the **Smart Multimodal Commute Advisor**, built with React and interactive mapping tools. It provides a user-friendly interface to predict commute times, visualize routes, and submit feedback.

---

## 🚀 Getting Started

### Prerequisites
-   [Node.js](https://nodejs.org/) (v16+)
-   npm or yarn

### Installation
1.  Navigate to the directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

### Running the App
Start the development server:
```bash
npm start
```
The app should automatically open at [http://localhost:3000](http://localhost:3000).

---

## 🛠️ Key Libraries

-   **React**: UI Library.
-   **Leaflet & React-Leaflet**: Powering the interactive map for route selection.
-   **Axios**: For communicating with the FastAPI backend.
-   **Lucide React**: For sleek, modern icons.

---

## 🎨 UI Features

-   **Interactive Map**: Clickable markers and route visualizations for Bangalore areas.
-   **Preference Selection**: Choose time of day, day type, and congestion levels.
-   **Real-time Predictions**: Instant travel time forecasts for Bus, Metro, Cab, and Two-Wheeler.
-   **Smart Comparison**: Visual highlights for the fastest vs. slowest modes.
-   **XAI Explanations**: Popover/sections explaining the logic behind the "Recommended Mode".
-   **Feedback Modal**: Simple interface to submit real-trip data.

---

## 📂 Structure

-   `src/components/`: Reusable UI components (Map, Selection Form, Result Cards).
-   `src/api/`: Axios configurations and endpoint calls.
-   `src/assets/`: Styles (CSS) and static images.
-   `src/App.js`: Main layout and state management.

---

## 🔧 Troubleshooting

-   **Map not loading**: Ensure you have an active internet connection to fetch Leaflet tiles.
-   **Backend Connection Error**: Verify the FastAPI backend is running on `http://localhost:8000`. You can change the base URL in `src/api/config.js` if necessary.
