const renderChartExpenses = (data, labels) => {
  let ctxe = document.getElementById("myChartExpenses").getContext("2d");
  let myExpensesChart = new Chart(ctxe, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expenses",
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
        text: "Expenses per category",
      },
    },
  });
};

const getExpenseChartData = () => {
  fetch("/expenses/expense_category_summary")
    .then((res) => res.json())
    .then((results) => {
      const categoryData = results.expense_category_data;
      const labels = Object.keys(categoryData);
      const data = Object.values(categoryData);
      renderChartExpenses(data, labels);
    });
};

window.onload = getExpenseChartData();
