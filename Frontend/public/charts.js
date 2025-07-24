document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch("/api/garbage-data"); // Fetch data from API
        const garbageData = await response.json();

        const dateWiseGarbage = {}; // Store garbage weight grouped by date

        // Get today's date and last week's date
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Normalize to midnight
        const lastWeek = new Date(today);
        lastWeek.setDate(today.getDate() - 6); // Include today in the 7-day range

        console.log("Filtering from:", lastWeek.toISOString(), "to", today.toISOString());
        console.log("Raw Data:", garbageData);

        garbageData.forEach((item) => {
            const recordDate = new Date(item.timestamp); // Convert timestamp to Date object
            recordDate.setMinutes(recordDate.getMinutes() + recordDate.getTimezoneOffset()); // Adjust for timezone
            const date = recordDate.toISOString().split("T")[0]; // Extract date (YYYY-MM-DD)

            if (recordDate >= lastWeek && recordDate <= today) {
                if (!dateWiseGarbage[date]) {
                    dateWiseGarbage[date] = 0;
                }
                dateWiseGarbage[date] += parseFloat(item.weight_kg) || 0; // Ensure proper summation
            }
        });

        const labels = Object.keys(dateWiseGarbage).sort(); // Sorted Dates
        const data = labels.map(date => dateWiseGarbage[date]); // Get corresponding weights

        if (labels.length === 0) {
            console.warn("No data available for the past week.");
        }

        // ✅ Bar Chart (Week's Data) - Click anywhere to open full data
        const barChart = new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Garbage Weight (kg)",
                    data: data,
                    backgroundColor: "rgba(75, 192, 192, 0.6)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                onClick: () => {
                    window.location.href = "graph_show.html"; // Redirects without filtering
                },
                scales: {
                    x: { title: { display: true, text: "Date" } },
                    y: { title: { display: true, text: "Weight (kg)" } }
                }
            }
        });

        // ✅ Line Chart (Week's Data)
        new Chart(document.getElementById("pieChart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Garbage Weight (kg)",
                    data: data,
                    borderColor: "blue",
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: { responsive: true }
        });

    } catch (error) {
        console.error("Error fetching garbage data:", error);
    }
});
