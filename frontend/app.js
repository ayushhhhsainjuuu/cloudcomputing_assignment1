const API_URL = "https://diet-function-ayush01-bqbadffegte2csby.canadacentral-01.azurewebsites.net/api/DietAnalysisAPI";

let barChartInstance;
let pieChartInstance;
let lineChartInstance;

async function loadDashboard() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    document.getElementById("execTime").textContent = `${data.execution_time_ms} ms`;
    document.getElementById("rowCount").textContent = data.summary.rows;
    document.getElementById("colCount").textContent = data.summary.columns;

    renderBarChart(data.charts.bar);
    renderPieChart(data.charts.pie);
    renderLineChart(data.charts.line);
  } catch (error) {
    console.error("Error loading dashboard:", error);
    alert("Failed to fetch dashboard data.");
  }
}

function renderBarChart(chartData) {
  const ctx = document.getElementById("barChart").getContext("2d");

  if (barChartInstance) {
    barChartInstance.destroy();
  }

  barChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Count",
          data: chartData.values,
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

function renderPieChart(chartData) {
  const ctx = document.getElementById("pieChart").getContext("2d");

  if (pieChartInstance) {
    pieChartInstance.destroy();
  }

  pieChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          data: chartData.values
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

function renderLineChart(chartData) {
  const ctx = document.getElementById("lineChart").getContext("2d");

  if (lineChartInstance) {
    lineChartInstance.destroy();
  }

  lineChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Values",
          data: chartData.values,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}

document.getElementById("refreshBtn").addEventListener("click", loadDashboard);

loadDashboard();