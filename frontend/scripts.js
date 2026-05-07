let selectedWorkloadId = null; // global variable to store the selected workload id
let workLoadCache = {}; // global variable to cache workload data for quick access when populating the form

function transformToGantt(workload) {
  return {
    id: String(workload.id),
    name: workload.module_name,
    start: workload.start_date,
    end: workload.end_date,
    progress: 0,
    custom_class: `bar-task-${workload.id}`,
  };
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
  document.getElementById("delete_btn").style.display = "none";
  document.getElementById("workload_form").reset();
  selectedWorkloadId = null;
  document.getElementById("submit_btn").textContent = "Add Workload";
}

function populateForm(workload) {
  // function to populate form with existing workload data when a Gantt bar is clicked
  document.getElementById("module_name").value = workload.module_name;
  document.getElementById("academic_year").value = workload.academic_year;
  document.getElementById("term_or_semester").value = workload.term_or_semester;
  document.getElementById("study_type").value = workload.study_type;
  document.getElementById("start_date").value = workload.start_date;
  document.getElementById("end_date").value = workload.end_date;
  document.getElementById("notes").value = workload.notes || "";
  document.getElementById("chart_colour").value = workload.chart_colour;
  selectedWorkloadId = workload.id;
  document.getElementById("submit_btn").textContent = "Update Module";
  document.getElementById("delete_btn").style.display = "block";
}

function loadWorkLoads() {
  // function to load workload data from the backend API, populate the cache, and initialise the Gantt chart
  fetch("http://localhost:8000/workloads/")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((workload) => {
        workLoadCache[String(workload.id)] = workload;
      });

      const ganttData = data.map(transformToGantt);

      // Inject dynamic bar colours using Frappe CSS variables
      const oldStyle = document.getElementById("gantt_dynamic_styles");
      if (oldStyle) oldStyle.remove();

      const styleEl = document.createElement("style");
      styleEl.id = "gantt_dynamic_styles";
      styleEl.textContent = data
        .map(
          (w) => `
          .gantt .bar-task-${w.id} {
              --g-bar-color: ${w.chart_colour} !important;
          }
      `,
        )
        .join("");
      document.head.appendChild(styleEl);

      document.getElementById("gantt_chart").innerHTML = "";
      new Gantt("#gantt_chart", ganttData, {
        on_click: (task) => {
          const workload = workLoadCache[task.id];
          if (workload) {
            populateForm(workload);
          } else {
            console.error("Workload data not found for task id:", task.id);
          }
        },
      });
    })
    .catch((error) => console.error("Error fetching workloads:", error));
}

function submitForm() {
  // function to handle form submission for adding or updating a workload
  const formData = getFormData();
  const url = selectedWorkloadId
    ? `http://localhost:8000/workloads/${selectedWorkloadId}/`
    : "http://localhost:8000/workloads/";
  const method = selectedWorkloadId ? "PUT" : "POST";
  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Workload submitted successfully:", data);
      loadWorkLoads(); // Reload the Gantt chart
      clearForm(); // Clear the form
    })
    .catch((error) => console.error("Error submitting workload:", error));
}

function deleteWorkload() {
  // function to handle deletion of a workload
  if (!selectedWorkloadId) {
    console.error("No workload selected for deletion.");
    return;
  }
  fetch(`http://localhost:8000/workloads/${selectedWorkloadId}/`, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        console.log("Workload deleted successfully.");
        loadWorkLoads(); // Reload the Gantt chart
        clearForm(); // Clear the form
      } else {
        console.error("Error deleting workload.");
      }
    })
    .catch((error) => console.error("Error deleting workload:", error));
}

// Initialise the Gantt chart when the page loads
document.addEventListener("DOMContentLoaded", () => {
  loadWorkLoads();
  document.getElementById("submit_btn").addEventListener("click", submitForm);
  document.getElementById("clear_btn").addEventListener("click", clearForm);
  document
    .getElementById("delete_btn")
    .addEventListener("click", deleteWorkload);
});
