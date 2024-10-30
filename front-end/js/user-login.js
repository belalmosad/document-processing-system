document
  .getElementById("login-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); 

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:3001/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;

        sessionStorage.setItem("jwt", token);

        window.location.href = "user-dashboard.html";
      } else {
        const errorData = await response.json();
        document.getElementById("response-message").innerText =
          errorData.message || "Login failed: Invalid credentials";
      }
    } catch (error) {
      document.getElementById("response-message").innerText =
        "Error logging in: " + error.message;
    }
  });
