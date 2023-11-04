const columnHeaders = [
    {title: "Curve Label", field: "curve_label", visible: false, clipboard: false},
    {title:"Num Cycles", field:"num_cycles"},
    {title:"Max Stress (MPa)", field:"max_stress"}, 
]

const currentUrl = window.location.href;
const apiURL = '/api/fatigue/'.concat(id_from_url(currentUrl))

console.log(apiURL)

var table = new Tabulator("#fatigue-table", {
    ajaxURL: apiURL,
    layout: "fitColumns",
    pagination:false,
 	columns: columnHeaders,
});

function id_from_url(url) {
    // Split the URL by the forward slash character.
    const urlSegments = url.split("/");
  
    // Get the last element of the split array.
    const lastSegment = urlSegments[urlSegments.length - 1];
  
    // If the last element contains a query string or fragment, remove everything after the first occurrence of either character.
    const lastString = lastSegment.split("?")[0].split("#")[0];
  
    return lastString;
  }
  