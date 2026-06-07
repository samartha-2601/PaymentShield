import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [dbStatus, setDbStatus] = useState("Checking...");

  useEffect(() => {
    api
      .get("/health/db")
      .then(() => {
        setDbStatus("Connected");
      })
      .catch(() => {
        setDbStatus("Disconnected");
      });
  }, []);

  const handlePayment = async () => {
    try {
      const response = await api.post("/payments/checkout");

      window.location.href = response.data.checkout_url;
    } catch (error) {
      console.error(error);
      alert("Unable to create checkout session");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>PaymentShield</h1>

      <h2>System Status</h2>

      <p>Database: {dbStatus}</p>

      <p>Payments: 0</p>

      <p>Alerts: 0</p>

      <button
        onClick={handlePayment}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        Make Test Payment
      </button>
    </div>
  );
}

export default App;