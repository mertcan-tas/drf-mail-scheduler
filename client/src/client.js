import axios from "axios";

const API_BASE_URL = "http://localhost/api";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default client;