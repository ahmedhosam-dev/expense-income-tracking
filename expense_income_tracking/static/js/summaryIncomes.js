const renderChart = (data, labels) => {
  let ctx = document.getElementById("myChartIncomes").getContext("2d");
  let myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months incomes",
          data: data,
          backgroundColor: [
            "rgba(255, 26, 104, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(0, 0, 0, 0.2)",
          ],
          borderColor: [
            "rgba(255, 26, 104, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(0, 0, 0, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Incomes per source",
      },
    },
  });
};

const getChartData = () => {
  fetch("/income/income_source_summary")
    .then((res) => res.json())
    .then((results) => {
      const sourceData = results.income_source_data;
      const labels = Object.keys(sourceData);
      const data = Object.values(sourceData);
      renderChart(data, labels);
    });
};

window.onload = getChartData();
