let mountainMarkerLayer;

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatMeters(value) {
  return value === null || value === undefined ? "-" : `${value} m`;
}

function createPopupContent(mountain) {
  return `
    <h3 class="popup-title">${escapeHtml(mountain.ch_mt_name)}</h3>
    <dl class="popup-list">
      <div class="popup-row">
        <dt class="popup-label">路線</dt>
        <dd>${escapeHtml(mountain.ch_trail_name)}</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">長度</dt>
        <dd>${escapeHtml(mountain.length_km)} km</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">海拔落差</dt>
        <dd>${formatMeters(mountain.elevation)}</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">最低海拔</dt>
        <dd>${formatMeters(mountain.elevation_min_m)}</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">最高海拔</dt>
        <dd>${formatMeters(mountain.elevation_max_m)}</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">行政區</dt>
        <dd>${escapeHtml(mountain.country)}</dd>
      </div>
    </dl>
  `;
}

async function fetchMountains(apiBaseUrl) {
  const response = await fetch(`${apiBaseUrl}/api/mountains`);
  if (!response.ok) {
    throw new Error(`山岳資料載入失敗 (${response.status})`);
  }

  return response.json();
}

function addMountainMarkers(map, mountains, onMountainSelected) {
  mountainMarkerLayer.clearLayers();

  mountains.forEach((mountain) => {
    if (mountain.latitude === null || mountain.longitude === null) {
      return;
    }

    const marker = L.marker([mountain.latitude, mountain.longitude])
      .bindPopup(createPopupContent(mountain))
      .on("click", () => onMountainSelected(mountain));

    marker.addTo(mountainMarkerLayer);
  });

  if (mountainMarkerLayer.getLayers().length > 0) {
    map.fitBounds(mountainMarkerLayer.getBounds(), { padding: [24, 24] });
  }
}

async function initTaiwanMap({ mapElementId, apiBaseUrl, onMountainSelected }) {
  const statusElement = document.getElementById("map-status");
  const map = L.map(mapElementId).setView([23.75, 121.05], 8);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  mountainMarkerLayer = L.layerGroup().addTo(map);

  try {
    const mountains = await fetchMountains(apiBaseUrl);
    addMountainMarkers(map, mountains, onMountainSelected);

    if (statusElement) {
      statusElement.textContent = `已從 API 載入 ${mountains.length} 條百岳路線。`;
    }
  } catch (error) {
    console.error(error);
    if (statusElement) {
      statusElement.textContent =
        "山岳資料載入失敗，請確認 backend API 是否已啟動。";
      statusElement.classList.add("status-error");
    }
  }
}

