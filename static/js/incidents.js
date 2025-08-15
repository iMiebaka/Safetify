document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/incidents/?ordering=-created_at")
    .then((r) => r.json())
    .then((items) => {
      const rows = document.getElementById("rows");
      items.forEach((i) => {
        const el = document.createElement("div");
        el.className = "list-group-item";
        el.innerText = `#${i.id} — ${i.title} — status: ${i.status} — risk: ${i.risk_score}`;

        // const link = document.createElement("a");
        // link.setAttribute("href", `/incident/${i.id}`);
        // link.innerText = `#${i.id} — ${i.title} — status: ${i.status} — risk: ${i.risk_score}`;
        // el.appendChild(link);
        rows.appendChild(el);
      });
    });
  const form = document.getElementById("incidentForm");
  const getLocationBtn = document.getElementById("getLocationBtn");
  const submitBtn = form.querySelector('button[type="submit"]');
  const submitText = document.getElementById("submitText");
  const spinner = document.getElementById("spinner");

  // Handle current location button
  getLocationBtn.addEventListener("click", function () {
    if (navigator.geolocation) {
      getLocationBtn.disabled = true;
      getLocationBtn.innerHTML =
        '<i class="bi bi-geo-alt-fill"></i> Detecting location...';

      navigator.geolocation.getCurrentPosition(
        function (position) {
          document.getElementById("latitude").value =
            position.coords.latitude.toFixed(4);
          document.getElementById("longitude").value =
            position.coords.longitude.toFixed(4);
          getLocationBtn.innerHTML =
            '<i class="bi bi-check-circle"></i> Location captured';
          setTimeout(() => {
            getLocationBtn.innerHTML =
              '<i class="bi bi-geo-alt"></i> Use Current Location';
            getLocationBtn.disabled = false;
          }, 2000);
        },
        function (error) {
          alert("Error getting location: " + error.message);
          getLocationBtn.innerHTML = '<i class="bi bi-geo-alt"></i> Try Again';
          getLocationBtn.disabled = false;
        }
      );
    } else {
      alert("Geolocation is not supported by your browser");
    }
  });

  // Handle form submission
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Show loading state
    submitBtn.disabled = true;
    submitText.textContent = "Submitting...";
    spinner.classList.remove("d-none");

    // Prepare payload
    const payload = {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      severity: parseInt(document.getElementById("severity").value),
      location: [
        parseFloat(document.getElementById("longitude").value),
        parseFloat(document.getElementById("latitude").value),
      ],
    };

    // Submit to API
    fetch("/api/incidents/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}", // Django CSRF token
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw err;
          });
        }
        return response.json();
      })
      .then((data) => {
        // Show success message
        submitText.textContent = "Submitted!";
        setTimeout(() => {
          window.location.href = "/";
        }, 1000);
      })
      .catch((error) => {
        console.error("Error:", error);
        submitBtn.disabled = false;
        submitText.textContent = "Submit Report";
        spinner.classList.add("d-none");

        // Show error message
        let errorMsg = "Failed to submit incident";
        if (error.detail) {
          errorMsg += ": " + error.detail;
        } else if (error.message) {
          errorMsg += ": " + error.message;
        }
        alert(errorMsg);
      });
  });
});
