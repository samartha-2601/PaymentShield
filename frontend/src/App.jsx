import { useEffect, useState } from "react";
import api from "./services/api";

function App() {

  const [dbStatus, setDbStatus] = useState("Checking...");
  const [summary, setSummary] = useState(null);
  const [payments, setPayments] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const loadDashboard = () => {

    api.get("/dashboard/summary")
      .then((response) => {
        setSummary(response.data);
      });

    api.get("/data/payments")
      .then((response) => {
        setPayments(response.data);
      });

    api.get("/data/alerts")
      .then((response) => {
        setAlerts(response.data);
      });
  };

  useEffect(() => {

    api.get("/health/db")
      .then(() => setDbStatus("Connected"))
      .catch(() => setDbStatus("Disconnected"));

    loadDashboard();

  }, []);

  const investigateAlert = async (alertId) => {

    await api.put(
      `/data/alerts/${alertId}/investigate`
    );

    loadDashboard();
  };

  const resolveAlert = async (alertId) => {

    await api.put(
      `/data/alerts/${alertId}/resolve`
    );

    loadDashboard();
  };

  const createPayment = async () => {

    const response = await api.post(
      "/payments/checkout"
    );

    window.location.href =
      response.data.checkout_url;
  };

  return (
    <div style={{ padding: "40px" }}>

      <h1>PaymentShield</h1>

      <button
        onClick={createPayment}
        style={{
          marginBottom: "20px",
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        Make Test Payment
      </button>

      <h2>System Status</h2>

      <p>Database: {dbStatus}</p>

      <hr />

      <h2>Fraud Dashboard</h2>

      <p>Payments: {summary?.payments || 0}</p>
      <p>Revenue: ${summary?.revenue || 0}</p>
      <p>Alerts: {summary?.alerts || 0}</p>

      <hr />

      <h2>Recent Payments</h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          width: "100%"
        }}
      >
        <thead>
          <tr>
            <th>Email</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Risk Score</th>
          </tr>
        </thead>

        <tbody>

          {payments.map((payment) => (

            <tr key={payment.id}>

              <td>{payment.email}</td>

              <td>${payment.amount}</td>

              <td>{payment.status}</td>

              <td
                style={{
                  color:
                    payment.risk_score >= 50
                      ? "red"
                      : payment.risk_score >= 25
                      ? "orange"
                      : "green",
                  fontWeight: "bold"
                }}
              >
                {payment.risk_score}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

      <hr />

      <h2>Recent Alerts</h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          width: "100%"
        }}
      >
        <thead>
          <tr>
            <th>Severity</th>
            <th>Type</th>
            <th>Status</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>

          {alerts.map((alert) => (

            <tr key={alert.id}>

              <td>{alert.severity}</td>

              <td>{alert.type}</td>

              <td
                style={{
                  fontWeight: "bold",
                  color:
                    alert.status === "OPEN"
                      ? "orange"
                      : alert.status === "INVESTIGATING"
                      ? "dodgerblue"
                      : "limegreen"
                }}
              >
                {alert.status}
              </td>

              <td>{alert.description}</td>

              <td>

                <button
                  onClick={() =>
                    investigateAlert(alert.id)
                  }
                >
                  Investigate
                </button>

                <button
                  onClick={() =>
                    resolveAlert(alert.id)
                  }
                  style={{
                    marginLeft: "10px"
                  }}
                >
                  Resolve
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default App;