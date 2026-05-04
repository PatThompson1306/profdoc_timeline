// global variable to store the selected workload id
let selectedWorkloadId = null;

function transformToGantt(workload) {
  // function to transform workload data frappe gantt chart formatted json
  return {
    id: String(workload.id),
    name: workload.module_name,
    start: workload.start_date,
    end: workload.end_date,
    progress: 0,
  };
}

function loadWorkLoads() {
  // function to fetch workload data from backend and transform it to Gantt chart formatted json
  // calls the transformToGantt function for each workload and returns an array of Gantt chart formatted json
  fetch("http://localhost:8000/workloads/")
    .then((response) => response.json())
    .then((data) => {
      const ganttData = data.map(transformToGantt);
      //console.log("Gantt Data:", ganttData);
      // Initialize the Gantt chart with the transformed data
      new Gantt("#gantt_chart", ganttData);
    })
    .catch((error) => console.error("Error fetching workload data:", error));
}

function getFormData() {
  // function to get form data and return it as an object
  return {
    module_name: document.getElementById("module_name").value,
    academic_year: document.getElementById("academic_year").value,
    term_or_semester: document.getElementById("term_or_semester").value,
    study_type: document.getElementById("study_type").value,
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
    chart_colour: document.getElementById("chart_colour").value,
    notes: document.getElementById("notes").value,
  };
}

function clearForm() {
  // function to clear form data
  document.getElementById("workload_form").reset();
  selectedWorkloadId = null;
  document.getElementById("submit_btn").textContent = "Add Workload";
}

//populateForm(workload) — fills the form with an existing workload's data when a Gantt bar is clicked, sets selectedWorkloadId, changes submit button text to "Update Module"

//submitForm() — reads selectedWorkloadId to decide POST vs PUT, calls the API, then reloads the Gantt and clears the form on success

loadWorkLoads();

document
  .getElementById("submit_btn")
  .addEventListener("click", () => console.log(getFormData()));

document.getElementById("clear_btn").addEventListener("click", clearForm);
