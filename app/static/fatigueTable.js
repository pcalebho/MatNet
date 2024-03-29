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
  const ksi_to_MPa = 6.89476;

  let option_label = label;
  if (type == "Mean Stress: "){
    option_label = Math.round(option_label*ksi_to_MPa)
  }
  optionElement.textContent = type.concat(option_label);

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
    clipboard: "copy",
    clipboardCopyConfig:{
        columnHeaders:false, //do not include column headers in clipboard output
        columnGroups:false, //do not include column groups in column headers for printed table
        rowGroups:false, //do not include row groups in clipboard output
        columnCalcs:false, //do not include column calculation rows in clipboard output
        dataTree:false, //do not include data tree in printed table
        formatCells:false, //show raw cell values without formatter
    },
});     

table.on("tableBuilt", updateFilter());

document.getElementById("filter-field").addEventListener("change", updateFilter);
document.getElementById("copy-btn").addEventListener("click", copyTable)

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
  
  function copyTable(){
    console.log('hi')
    table.copyToClipboard("active"); //copy the currently selected rows to the clipboard
  }