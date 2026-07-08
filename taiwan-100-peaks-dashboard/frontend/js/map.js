const mountainRoutes = [
  {
    hiking_note_id: 429,
    ch_mt_name: "武陵四秀",
    ch_trail_name: "桃山步道",
    trail_name: "tao_mountain",
    latitude: 24.43251,
    longitude: 121.30463,
    length_km: 7.9,
    elevation_min_m: 1883,
    elevation_max_m: 3325,
    elevation_diff_m: 1442,
    country: "臺中市和平區,新竹縣尖石鄉",
  },
  {
    hiking_note_id: 1746,
    ch_mt_name: "武陵四秀",
    ch_trail_name: "桃山喀拉業",
    trail_name: "tao_kalaye",
    latitude: 24.45003069,
    longitude: 121.3213877,
    length_km: 9,
    elevation_min_m: 1860,
    elevation_max_m: 3325,
    elevation_diff_m: 1465,
    country: "臺中市和平區,新竹縣尖石鄉,宜蘭縣大同鄉",
  },
  {
    hiking_note_id: 1737,
    ch_mt_name: "武陵四秀",
    ch_trail_name: "武陵二秀(池有,品田)",
    trail_name: "chiyou_pintian",
    latitude: 24.4282,
    longitude: 121.2668,
    length_km: 10.1,
    elevation_min_m: 1860,
    elevation_max_m: 3524,
    elevation_diff_m: 1664,
    country: "臺中市和平區,新竹縣尖石鄉",
  },
  {
    hiking_note_id: 1750,
    ch_mt_name: "北大武山",
    ch_trail_name: "北大武山步道",
    trail_name: "mt_beidawu",
    latitude: 22.62706,
    longitude: 120.7613,
    length_km: 12,
    elevation_min_m: 1550,
    elevation_max_m: 3090,
    elevation_diff_m: 1540,
    country: "屏東縣瑪家鄉,屏東縣泰武鄉,臺東縣金峰鄉",
  },
  {
    hiking_note_id: 1761,
    ch_mt_name: "塔關山",
    ch_trail_name: "塔關山登山步道",
    trail_name: "mt_taguan",
    latitude: 23.2519,
    longitude: 120.94119,
    length_km: 2.2,
    elevation_min_m: 2580,
    elevation_max_m: 3222,
    elevation_diff_m: 642,
    country: "高雄市桃源區,臺東縣海端鄉",
  },
  {
    hiking_note_id: 288,
    ch_mt_name: "合歡山",
    ch_trail_name: "合歡北峰步道",
    trail_name: "hehuan_north",
    latitude: 24.18152,
    longitude: 121.28167,
    length_km: 2,
    elevation_min_m: 2975,
    elevation_max_m: 3422,
    elevation_diff_m: 447,
    country: "南投縣仁愛鄉,花蓮縣秀林鄉",
  },
  {
    hiking_note_id: 68,
    ch_mt_name: "玉山",
    ch_trail_name: "玉山前峰登山山徑",
    trail_name: "mt_jade_front",
    latitude: 23.4756,
    longitude: 120.91765,
    length_km: 3.5,
    elevation_min_m: 2610,
    elevation_max_m: 3239,
    elevation_diff_m: 629,
    country: "南投縣信義鄉,嘉義縣阿里山鄉",
  },
];

function createPopupContent(route) {
  return `
    <h3 class="popup-title">${route.ch_mt_name}</h3>
    <dl class="popup-list">
      <div class="popup-row">
        <dt class="popup-label">路線</dt>
        <dd>${route.ch_trail_name}</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">長度</dt>
        <dd>${route.length_km} km</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">最低海拔</dt>
        <dd>${route.elevation_min_m} m</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">最高海拔</dt>
        <dd>${route.elevation_max_m} m</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">海拔落差</dt>
        <dd>${route.elevation_diff_m} m</dd>
      </div>
      <div class="popup-row">
        <dt class="popup-label">行政區</dt>
        <dd>${route.country}</dd>
      </div>
  `;
}

function initTaiwanMap(elementId) {
  const map = L.map(elementId).setView([23.75, 121.05], 8);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  mountainRoutes
    .forEach((route) => {
      L.marker([route.latitude, route.longitude])
        .addTo(map)
        .bindPopup(createPopupContent(route));
    });

  const statusElement = document.getElementById("map-status");
  if (statusElement) {
    statusElement.textContent = `已載入 ${mountainRoutes.length} 條百岳單攻路線。`;
  }
}

