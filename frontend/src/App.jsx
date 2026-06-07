import { useEffect, useState } from "react";
import api from "./services/api";

function App() {

  const [dbStatus, setDbStatus] = useState("Checking...");
  const [summary, setSummary] = useState(null);
  const [payments, setPayments] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {

    api.get("/health/db")
      .then(() => setDbStatus("Connected"))
      .catch(() => setDbStatus("Disconnected"));

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

  }, []);

  return (
    <div style={{ padding: "40px" }}>

      <h1>PaymentShield</h1>

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
            <th>Description</th>
          </tr>
        </thead>

        <tbody>

          {alerts.map((alert) => (

            <tr key={alert.id}>
              <td>{alert.severity}</td>
              <td>{alert.type}</td>
              <td>{alert.description}</td>
            </tr>

          ))}

        </tbody>

      </table>



    </div>
  );
}

export default App;