// components/BarChart.js
import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BarChart = ({ data }) => {
  const years = data.map((item) => item.year);
  const marketSizes = data.map((item) => item.market_size);

  const chartData = {
    labels: years,
    datasets: [
      {
        label: "Market Size (billion USD)",
        data: marketSizes,
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Market Size Over Years",
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default BarChart;
