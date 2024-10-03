import React, { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

const CandlestickChart = () => {
  const chartContainerRef = useRef();
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch candlestick data from the backend
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:80/candlestick");
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (data.length === 0) return;

    // Create the chart after the data has been fetched
    const chart = createChart(chartContainerRef.current, {
      width: 600,
      height: 400,
    });
    const candlestickSeries = chart.addCandlestickSeries();

    // Set data for the candlestick series
    candlestickSeries.setData(
      data.map((item) => ({
        time: item.time, // Should be in "YYYY-MM-DD" format or Unix timestamp
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
      }))
    );

    return () => {
      chart.remove();
    };
  }, [data]);

  return <div ref={chartContainerRef} />;
};

export default CandlestickChart;
