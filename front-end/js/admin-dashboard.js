async function loadAuditTrail() {
  const token = sessionStorage.getItem("jwt");
  if (!token) {
    document.getElementById("response-message").innerText =
      "Not authorized. Please log in.";
    return;
  }

  try {
    const response = await fetch("http://localhost:3001/admin/audit", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const auditData = await response.json();
      displayAuditData(auditData);
    } else {
      document.getElementById("response-message").innerText =
        "Failed to load audit data.";
    }
  } catch (error) {
    document.getElementById("response-message").innerText =
      "Error fetching audit data: " + error.message;
  }
}

function displayAuditData(data) {
  const tableBody = document
    .getElementById("audit-table")
    .querySelector("tbody");
  tableBody.innerHTML = "";

  data.forEach((entry) => {
    const row = document.createElement("tr");
    row.innerHTML = `
                    <td>${entry.id}</td>
                    <td>${entry.user_id}</td>
                    <td>${entry.action}</td>
                    <td>${entry.action_type}</td>
                    <td>${new Date(entry.timestamp).toLocaleString()}</td>
                `;
    tableBody.appendChild(row);
  });
}

document
  .getElementById("signup-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const token = sessionStorage.getItem("jwt");
    if (!token) {
      document.getElementById("response-message").innerText =
        "Not authorized. Please log in.";
      return;
    }

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    try {
      const response = await fetch("http://localhost:3001/users/signup", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password, role }),
      });

      if (response.ok) {
        document.getElementById("response-message").innerText =
          "User created successfully!";
        document.getElementById("signup-form").reset();
      } else {
        const errorData = await response.json();
        console.log(response);
        document.getElementById("response-message").innerText =
          errorData.message || "Failed to create user.";
      }
    } catch (error) {
      document.getElementById("response-message").innerText =
        "Error creating user: " + error.message;
    }
  });

window.onload = loadAuditTrail;
