async function load() {
  try {
    const response = await fetch("/api/dashboard");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    document.getElementById("kpis").innerHTML = [
      [
        "Servers",
        data.kpis.servers,
        "3 regions · 2 active projects"
      ],
      [
        "vCPU Allocated",
        data.kpis.vcpu,
        "64% of regional capacity"
      ],
      [
        "Storage",
        data.kpis.storage,
        "21.4 TB available"
      ],
      [
        "Networks",
        data.kpis.networks,
        "All routing healthy"
      ]
    ]
      .map(
        item => `
          <div class="kpi">
            <small>${item[0]}</small>
            <div class="value">${item[1]}</div>
            <p>${item[2]}</p>
          </div>
        `
      )
      .join("");

    renderRows(data.servers);

    document.getElementById("regions").innerHTML = data.regions
      .map(
        region => `
          <div class="region">
            <div class="rhead">
              <span>${region.name}</span>
              <span>${region.utilization}%</span>
            </div>

            <div class="rsub">
              ${region.code} · ${region.servers} servers
            </div>

            <div class="rbar">
              <i style="width:${region.utilization}%"></i>
            </div>
          </div>
        `
      )
      .join("");

    return data;
  } catch (error) {
    console.error("Dashboard API error:", error);

    document.getElementById("kpis").innerHTML = `
      <div class="kpi">
        <small>STATUS</small>
        <div class="value">API Error</div>
        <p>Backend is not responding.</p>
      </div>
    `;

    document.getElementById("rows").innerHTML = `
      <tr>
        <td colspan="5">
          Unable to load server data.
        </td>
      </tr>
    `;
  }
}


function renderRows(rows) {
  const table = document.getElementById("rows");

  if (!rows || rows.length === 0) {
    table.innerHTML = `
      <tr>
        <td colspan="5">No servers found.</td>
      </tr>
    `;
    return;
  }

  table.innerHTML = rows
    .map(server => {
      const statusClass =
        server.state === "ACTIVE"
          ? "active"
          : "stopped";

      return `
        <tr>
          <td>
            <div class="name">${server.name}</div>
            <div class="sub">${server.id}</div>
          </td>

          <td>${server.region}</td>

          <td>
            <span class="pill ${statusClass}">
              ${server.state}
            </span>
          </td>

          <td>${server.flavor}</td>

          <td>${server.ip}</td>
        </tr>
      `;
    })
    .join("");
}


let dashboardData = null;

load().then(data => {
  if (!data) {
    return;
  }

  dashboardData = data;

  const searchInput =
    document.getElementById("search");

  searchInput.addEventListener("input", event => {
    const query = event.target.value
      .trim()
      .toLowerCase();

    if (!query) {
      renderRows(dashboardData.servers);
      return;
    }

    const filtered = dashboardData.servers.filter(server =>
      Object.values(server).some(value =>
        String(value)
          .toLowerCase()
          .includes(query)
      )
    );

    renderRows(filtered);
  });
});
