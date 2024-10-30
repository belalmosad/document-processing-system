const token = sessionStorage.getItem("jwt");

document
  .getElementById("search-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const searchKeyword = document.getElementById("search").value;

    try {
      const response = await fetch("http://localhost:3001/documents/search", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ search: searchKeyword }),
      });

      if (response.ok) {
        const results = await response.json();
        displaySearchResults(results);
      }
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  });

function displaySearchResults(results) {
  const table = document.getElementById("search-results-table");
  const tableBody = table.querySelector("tbody");
  const emptyState = document.getElementById("search-empty-state");

  tableBody.innerHTML = "";
  if (results.length === 0) {
    table.style.display = "none";
    emptyState.style.display = "block";
  } else {
    results.forEach((doc) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                        <td>${doc.id}</td>
                        <td>${doc.filename}</td>
                        <td>${JSON.stringify(doc.keywords)}</td>
                    `;
      tableBody.appendChild(row);
    });
    table.style.display = "table";
    emptyState.style.display = "none";
  }
}

async function loadMyFiles() {
  try {
    const response = await fetch(
      "http://localhost:3001/documents/metadata/author/all",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (response.ok) {
      const files = await response.json();
      displayMyFiles(files);
    }
  } catch (error) {
    console.error("Error fetching my files:", error);
  }
}

function displayMyFiles(files) {
  const tableBody = document
    .getElementById("my-files-table")
    .querySelector("tbody");
  const emptyState = document.getElementById("my-files-empty-state");

  tableBody.innerHTML = "";
  if (files.length === 0) {
    emptyState.style.display = "block";
  } else {
    files.forEach((doc) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                        <td>${doc.id}</td>
                        <td>${JSON.stringify(doc.keywords)}</td>
                        <td>${doc.document_type}</td>
                        <td>${doc.size}</td>
                        <td>${doc.filename}</td>
                    `;
      tableBody.appendChild(row);
    });
    emptyState.style.display = "none";
  }
}

document
  .getElementById("single-document-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const documentId = document.getElementById("document-id").value;

    try {
      const response = await fetch(
        `http://localhost:3001/document/metadata/${documentId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.ok) {
        const doc = await response.json();
        displaySingleDocument(doc);
      } else {
        displaySingleDocument(null); 
      }
    } catch (error) {
      console.error("Error fetching document metadata:", error);
    }
  });

function displaySingleDocument(doc) {
  const table = document.getElementById("single-document-table");
  const tableBody = table.querySelector("tbody");
  const emptyState = document.getElementById("single-document-empty-state");

  tableBody.innerHTML = "";
  if (!doc) {
    table.style.display = "none";
    emptyState.style.display = "block";
  } else {
    tableBody.innerHTML = `
                    <tr>
                        <td>${doc.id}</td>
                        <td>${JSON.stringify(doc.keywords)}</td>
                        <td>${doc.document_type}</td>
                        <td>${doc.size}</td>
                        <td>${doc.filename}</td>
                    </tr>
                `;
    table.style.display = "table";
    emptyState.style.display = "none";
  }
}

document
  .getElementById("upload-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:3001/documents/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const responseMessage = document.getElementById(
        "upload-response-message"
      );
      console.log(response);
      if (response.ok) {
        responseMessage.innerText = "Document uploaded successfully!";
        responseMessage.style.color = "green";
      } else {
        responseMessage.innerText = "Failed to upload document.";
        responseMessage.style.color = "red";
      }
      responseMessage.style.display = "block";
    } catch (error) {
      console.error("Error uploading document:", error);
    }
  });

document
  .getElementById("get-url-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const documentId = document.getElementById("document-id-url").value;

    try {
      const response = await fetch(
        `http://localhost:3001/documents/${documentId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      const documentUrl = document.getElementById("document-url");
      if (response.ok) {
        const fileBlob = await response.blob();

        const fileUrl = URL.createObjectURL(fileBlob);

        documentUrl.innerHTML = `Document URL: <a href="${fileUrl}" target="_blank">Open Document</a>`;
        documentUrl.style.color = "blue";
      } else {
        documentUrl.innerText = "Failed to retrieve document URL.";
        documentUrl.style.color = "red";
      }
      documentUrl.style.display = "block";
    } catch (error) {
      console.error("Error fetching document URL:", error);
    }
  });

window.onload = loadMyFiles;
