// function to transform workload data frappe gantt chart formatted json
function transformToGantt(workload) {
  return {
    id: String(workload.id),
    name: workload.module_name,
    start: workload.start_date,
    end: workload.end_date,
    progress: 0,
  };
}

// function to fetch workload data from backend and transform it to Gantt chart formatted json
// calls the transformToGantt function for each workload and returns an array of Gantt chart formatted json
function loadWorkLoads() {
  fetch("http://localhost:8000/workloads/")
    .then((response) => response.json())
    .then((data) => {
      const ganttData = data.map(transformToGantt);
      console.log("Gantt Data:", ganttData);
    })
    .catch((error) => console.error("Error fetching workload data:", error));
}

// call the loadWorkLoads function to fetch workload data and transform it to Gantt chart formatted json
loadWorkLoads();
