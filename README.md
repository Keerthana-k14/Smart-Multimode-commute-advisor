# 🚀 Smart Multimodal Commute Advisor

A sophisticated, AI-powered commute recommendation system designed to optimize urban travel. This application predicts travel times for various transport modes and suggests the most efficient route based on real-time conditions like congestion, time of day, and day of the week.

---

## 🌟 Key Features

-   **🤖 Multi-Modal Predictions**: Forecasts travel times for **Bus**, **Metro**, **Cab**, and **Two-Wheeler**.
-   **💡 Intelligent Recommendations**: Automatically suggests the fastest mode of transport for your specific journey.
-   **🔍 Explainable AI (XAI)**: Provides clear, human-readable explanations for why a particular mode was recommended.
-   **🗺️ Interactive Mapping**: Visualizes routes and areas using an integrated Leaflet map interface.
-   **📈 Feedback Loop**: A built-in feedback system to collect real-world data and improve prediction accuracy over time.
-   **🏙️ Bangalore-Centric**: Pre-configured with major hubs like Indiranagar, Whitefield, Koramangala, and more.

---

## 🛠️ Tech Stack

### Frontend
-   **Framework**: [React](https://reactjs.org/)
-   **Maps**: [Leaflet](https://leafletjs.org/) & [React-Leaflet](https://react-leaflet.js.org/)
-   **Icons**: [Lucide React](https://lucide.dev/)
-   **Styling**: Modern CSS with Glassmorphism effects
-   **API Client**: [Axios](https://axios-http.com/)

### Backend
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Server**: [Uvicorn](https://www.uvicorn.org/)
-   **ML Stack**: Scikit-Learn, Pandas, NumPy
-   **Visualization**: Matplotlib, Seaborn (for data analysis)

---

## 📂 Project Structure

```text
smart-commute-advisor/
├── backend/                # FastAPI Application
│   ├── api/                # API Routes & Schemas
│   ├── ml/                 # Machine Learning Models & Logic
│   ├── simulator/          # Traffic Simulation Logic
│   ├── explainer/          # XAI Logic for Recommendations
│   └── data/               # Datasets & User Feedback
├── frontend/               # React Application
│   ├── src/                # Components & UI Logic
│   └── public/             # Static Assets
└── notebooks/              # Data Science & EDA Notebooks
```

---

## 🚀 Getting Started

### Prerequisites
-   Python 3.8+
-   Node.js 16+
-   npm or yarn

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```
The application will open at `http://localhost:3000`.

---

## 📡 API Endpoints

-   `GET /routes`: Fetches available areas and road networks.
-   `POST /predict`: Predicts commute times and provides recommendations based on input (area, road, time, congestion).
-   `POST /feedback`: Submits user feedback to the system.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
