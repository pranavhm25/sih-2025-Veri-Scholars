document.getElementById("upload-btn").addEventListener("click", () => {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    const statusCard = document.getElementById("status-card");
    const statusMessage = document.getElementById("status-message");
    const nameEl = document.getElementById("name");
    const certIdEl = document.getElementById("certificate-id");
    const instEl = document.getElementById("institution");

    if (data.verification && data.verification.success) {
      statusCard.className = "status-card success";
      statusMessage.textContent = "✅ Certificate Verified!";
    } else {
      statusCard.className = "status-card fail";
      statusMessage.textContent = "❌ Does not EXIST!";
    }

    nameEl.textContent = data.extracted_data.name || "-";
    certIdEl.textContent = data.extracted_data.certificate_id || "-";
    instEl.textContent = data.extracted_data.institution || "-";

    statusCard.classList.remove("hidden");
  })
  .catch(err => {
    alert("Error uploading file: " + err);
  });
});
