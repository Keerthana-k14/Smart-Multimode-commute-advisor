import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" }
});

export const getRoutes    = ()        => API.get("/routes");
export const getPredict   = (data)    => API.post("/predict", data);
export const postFeedback = (data)    => API.post("/feedback", data);

export default API;