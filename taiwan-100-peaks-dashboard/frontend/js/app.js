const API_BASE_URL = window.API_BASE_URL || "http://localhost:8000";

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

