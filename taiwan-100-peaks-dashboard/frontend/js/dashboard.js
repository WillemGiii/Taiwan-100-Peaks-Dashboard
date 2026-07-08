let monthlyChart = null;

function initDashboard() {
  updateDashboardStatus("請點擊地圖上的山岳 Marker。");
}

function updateDashboardStatus(message, isError = false) {
  const statusElement = document.getElementById("dashboard-status");
  if (!statusElement) {
    return;
  }

  statusElement.textContent = message;
  statusElement.classList.toggle("status-error", isError);
}

function formatDuration(minutes) {
  if (minutes === null || minutes === undefined) {
    return "-";
  }

  const totalMinutes = Math.round(Number(minutes));
  const hours = Math.floor(totalMinutes / 60);
  const remainingMinutes = totalMinutes % 60;

  if (hours === 0) {
    return `${remainingMinutes} 分鐘`;
  }

  return `${hours} 小時 ${remainingMinutes} 分鐘`;
}

function formatDistance(km) {
  if (km === null || km === undefined) {
    return "-";
  }

  return `${Number(km).toFixed(2)} km`;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
}

function clearMonthlyChart() {
  if (monthlyChart) {
    monthlyChart.destroy();
    monthlyChart = null;
  }
}

function renderMonthlyChart(monthlyDistribution) {
  const canvas = document.getElementById("monthly-chart");
  if (!canvas) {
    return;
  }

  clearMonthlyChart();

  const labels = Array.from({ length: 12 }, (_, index) => `${index + 1} 月`);
  const monthCounts = new Map(
    monthlyDistribution.map((item) => [Number(item.month), Number(item.count)])
  );
  const values = labels.map((_, index) => monthCounts.get(index + 1) || 0);

  monthlyChart = new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "登山紀錄數量",
          data: values,
          borderColor: "#2f6f4e",
          backgroundColor: "rgba(47, 111, 78, 0.28)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
          },
        },
      },
    },
  });
}

function renderDashboard(data) {
  setText("dashboard-mountain-name", data.mountain_name || "-");
  setText("dashboard-trail-name", data.trail_name || "-");

  if (data.data_status === "insufficient_data") {
    setText("dashboard-duration", "-");
    setText("dashboard-distance", "-");
    clearMonthlyChart();
    updateDashboardStatus(
      data.message || "目前此山岳登山紀錄不足，暫時無法產生可靠統計。"
    );
    return;
  }

  setText("dashboard-duration", formatDuration(data.average_duration_minutes));
  setText("dashboard-distance", formatDistance(data.average_distance_km));
  renderMonthlyChart(data.monthly_distribution || []);
  updateDashboardStatus("已載入山岳統計資料。");
}

async function loadDashboard(apiBaseUrl, mountainId) {
  updateDashboardStatus("載入山岳統計資料中...");

  try {
    const parsedMountainId = Number(mountainId);
    if (!Number.isInteger(parsedMountainId)) {
      throw new Error(`Invalid mountain id: ${mountainId}`);
    }

    const response = await fetch(
      `${apiBaseUrl}/api/mountains/${parsedMountainId}/dashboard`
    );
    if (!response.ok) {
      throw new Error(`儀表板資料載入失敗 (${response.status})`);
    }

    const data = await response.json();
    renderDashboard(data);
  } catch (error) {
    console.error(error);
    clearMonthlyChart();
    updateDashboardStatus("儀表板資料載入失敗，請稍後再試。", true);
  }
}

