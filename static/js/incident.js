const fetchAllIncident = async () => {
  window.addEventListener("load", function () {
    document.getElementById("loadingBar").style.width = "100%";
  });

  const path = window.location.pathname;
  // Extract ID (last segment of URL)
  const incidentId = path.split("/").pop();
  // For real page loading:
  fetch(`/api/incidents/${incidentId}/`)
    .then((r) => r.json())
    .then((data) => {
      console.log(data);
      document.getElementById("incident-title").textContent = data.title;
      document.getElementById("incident-status").textContent =
        data.status.charAt(0).toUpperCase() + data.status.slice(1);
      document.getElementById(
        "incident-status"
      ).className = `badge badge-${data.status.replace(" ", "-")}`;

      document.getElementById(
        "incident-severity"
      ).textContent = `Level ${data.severity}`;
      document.getElementById(
        "severity-icon"
      ).className = `severity-indicator severity-${data.severity}`;

      document.getElementById("incident-risk").textContent =
        data.risk_score.toFixed(1);
      document.getElementById(
        "incident-location"
      ).textContent = `${data.location[0]}, ${data.location[1]}`;
      document.getElementById("incident-description").textContent =
        data.description;
      document.getElementById("incident-created").textContent = formatDate(
        data.created_at
      );
      document.getElementById("incident-updated").textContent = formatDate(
        data.updated_at
      );
      document.getElementById("incident-id").textContent = data.id;
    })
    .catch(() => {
      document.getElementById("error-el").setAttribute("hidden", "false");
    })
    .finally(() => {
      setTimeout(() => {
        document.getElementById("loadingBar").style.opacity = "0";
      }, 300);
    });
};

fetchAllIncident().then();
