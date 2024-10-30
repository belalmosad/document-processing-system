document
  .getElementById("admin-login-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const saCredentials = document.getElementById("sa-credentials").value;

    try {
      const response = await fetch("http://localhost:3001/admin/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ admin_cred: saCredentials }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        console.log(token);
        sessionStorage.setItem("jwt", token);
        window.location.href = "admin-dashboard.html";
      } else {
        document.getElementById("response-message").innerText =
          "Login failed: Invalid credentials";
      }
    } catch (error) {
      console.log(error);
      document.getElementById("response-message").innerText =
        "Error logging in: ";
    }
  });
