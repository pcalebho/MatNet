export let rowPopupFormatter = function(e, row, onRendered){
    let data = row.getData();
    let categories = convertArrayToString(data.categories, " | ");
    let compEleProp = data.component_elements_properties
    const entries = Object.entries(compEleProp)
    
    
    let container = document.createElement("div");
    let contents = "<strong style='font-size:1.2em;'>Additional Details</strong><br/><ul style='padding:0;  margin-top:10px; margin-bottom:0;'>";
    contents += "<li><strong>Categories:</strong> " + categories + "</li>";
    contents += "<li><strong>Component Elements:</strong><ul>";
    
    for (const [element, percentage] of entries){
        contents+= "<li>" + convertStr(element) + ": " + percentage + "</li>";
    }
    
    contents += "</ul>";
    contents += "</ul>";

    container.innerHTML = contents;

    return container;
};

function convertStr(str) {
    let eleName;
    let eleAbbr;
    
    const strParts = str.split("_");
    eleName = strParts[0];
    eleAbbr = strParts[1];

    eleName = eleName[0].toUpperCase() + eleName.slice(1);

    if (eleAbbr.length === 1) {
        eleAbbr = eleAbbr.toUpperCase();
    } else {
        let firstLetter = eleAbbr[0];
        eleAbbr = firstLetter.toUpperCase() + eleAbbr.slice(1); 
    }

    return eleName + "(" + eleAbbr + ")";
}

function convertArrayToString(array, delimiter) {
    let string = "";

    for (const item of array) {
        string += (item + delimiter);
    }

    return string.slice(0,string.length-3);
}