# 🐍 Smart Commute Advisor - Backend

The AI engine and API for the **Smart Multimodal Commute Advisor**, powered by **FastAPI** and **Scikit-Learn**. It manages route data, travel time predictions, and User Feedback Loop.

---

## 🚀 Getting Started

### Prerequisites
-   [Python 3.8+](https://www.python.org/downloads/)
-   pip (Python package installer)

### Installation
1.  Navigate to the directory:
    ```bash
    cd backend
    ```
2.  Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the API
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be live at [http://localhost:8000](http://localhost:8000).

---

## 📡 API Endpoints

-   `GET /`: Root message.
-   `GET /routes`: Fetches available areas and road networks.
-   `POST /predict`: Main inference endpoint for travel times.
-   `POST /feedback`: Saves user-reported data for future model training.

---

## 🧠 Core Logic

-   **ML Predictions**: Uses pre-trained Scikit-Learn models to forecast durations for Bus, Metro, Cab, and Two-Wheeler.
-   **XAI Explainer**: Generates human-readable rationales based on input parameters (e.g., "Metro is recommended due to high traffic congestion").
-   **Data Storage**: Feedback is currently logged in `backend/data/user_feedback.json`.

---

## 📂 Structure

-   `api/`: Pydantic models (schemas) and FastAPI routers.
-   `ml/`: The core commute duration prediction logic.
-   `explainer/`: Logic for Explainable AI (XAI).
-   `data/`: Static datasets and feedback storage.
-   `simulator/`: Traffic pattern generation utilities.
-   `main.py`: Application entry point.

---

## 🔧 Troubleshooting

-   **ModuleNotFoundError**: Ensure your virtual environment is active and all `requirements.txt` are installed.
-   **CORS Issues**: The backend is configured to allow all origins (`*`) by default, but you can restrict this in `main.py`.
