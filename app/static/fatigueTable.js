const columnHeaders = [
    {title: "Curve Label", field: "curve_label", visible: false, clipboard: false},
    {title:"Num Cycles", field:"num_cycles", hozAlign: "center", headerSort: false},
    {title:"Max Stress (MPa)", field:"max_stress", hozAlign: "center", headerSort: false},  
]

const currentUrl = window.location.href;
const apiURL = '/api/fatigue/'.concat(id_from_url(currentUrl))

async function getFatigueData() {
    const response = await fetch(apiURL);
    return await response.json();
}

const fatigueData = await getFatigueData()
const labels = fatigueData.labels

// Create the select widget element
const selectWidget = document.getElementById('filter-field');

// Add options to the select widget element
let type;
if (labels.some(value => value > 5)){
    type = "Mean Stress: "
} else {
    type = "Stress Ratio: "
}

for (const label of labels) {
  const optionElement = document.createElement('option');
  optionElement.value = label;
  optionElement.textContent = type.concat(label);

  selectWidget.appendChild(optionElement);
}



var table = new Tabulator("#fatigue-table", {
    ajaxURL: apiURL,
    layout: "fitData",
    rowHeight: 40,
    ajaxResponse: function(url, params, response) {
        // Assuming response is the entire API response object
        // var data = response.data || []; // Extract the "data" array
        return response.data || []; // Return the extracted array
    },
    pagination:false,
 	columns: columnHeaders,
});

updateFilter()

document.getElementById("filter-field").addEventListener("change", updateFilter);

function updateFilter() {
    let chosen_curve = selectWidget.value;
    table.setFilter("curve_label", "=", chosen_curve)
}

function id_from_url(url) {
    // Split the URL by the forward slash character.
    const urlSegments = url.split("/");
  
    // Get the last element of the split array.
    const lastSegment = urlSegments[urlSegments.length - 1];
  
    // If the last element contains a query string or fragment, remove everything after the first occurrence of either character.
    const lastString = lastSegment.split("?")[0].split("#")[0];
  
    return lastString;
  }
  