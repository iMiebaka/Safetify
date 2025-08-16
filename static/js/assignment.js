const fetchAssignment = async () => {
  window.addEventListener("load", function () {
    document.getElementById("loadingBar").style.width = "100%";
  });

  const path = window.location.pathname;
  // Extract ID (last segment of URL)
  const assignmentId = path.split("/").pop();
  // For real page loading:
  fetch(`/api/assignments/${assignmentId}/`)
    .then((r) => r.json())
    .then((data) => {
      console.log(data);

      document.getElementById("incident-title").textContent =
        data.incident.title;
      document.getElementById("incident-status").textContent =
        data.incident.status.charAt(0).toUpperCase() +
        data.incident.status.slice(1);
      document.getElementById(
        "incident-status"
      ).className = `badge badge-${data.incident.status.replace(" ", "-")}`;

      document.getElementById("technician-user").textContent =
        data.technician.user;
      document.getElementById("technician-phone").textContent =
        data.technician.phone;
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

fetchAssignment().then();
