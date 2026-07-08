function getDefaultApiBaseUrl() {
  const { protocol, hostname } = window.location;

  if (!hostname || protocol === "file:") {
    return "http://localhost:8000";
  }

  const apiHost = hostname.includes(":") ? `[${hostname}]` : hostname;
  return `${protocol}//${apiHost}:8000`;
}

const API_BASE_URL = window.API_BASE_URL || getDefaultApiBaseUrl();

document.addEventListener("DOMContentLoaded", () => {
  initDashboard();
  initTaiwanMap({
    mapElementId: "map",
    apiBaseUrl: API_BASE_URL,
    onMountainSelected: (mountain) => {
      loadDashboard(API_BASE_URL, mountain.hiking_note_id);
    },
  });
});

