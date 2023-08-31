var minMaxFilterEditor = function(cell, onRendered, success, cancel, editorParams){
    let end;

    //create elements
    let container = document.createElement("div");
    let start = document.createElement("input");
    let importance = document.createElement("input");

    //set attributes
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);    
    importance.setAttribute("type","range");
    importance.setAttribute("min",0);
    importance.setAttribute("max",10); 

    //set styles and classes
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";
    container.classList.add('custom-headerFilter')
    importance.classList.add('form-range')

    start.value = cell.getValue();

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    function buildValues(){ 
        success({
            start:start.value,
            end:end.value,
        });
    }

    function keypress(e){
        if(e.keyCode == 13){
            buildValues();
        }

        if(e.keyCode == 27){
            cancel();
        }
    }


    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);

    container.appendChild(importance);
    container.appendChild(start);
    container.appendChild(end);

    return container;
}

//custom max min filter function
function minMaxFilterFunction(headerValue, rowValue, rowData, filterParams){
//headerValue - the value of the header filter element
//rowValue - the value of the column in this row
//rowData - the data for the row being filtered
//filterParams - params object passed to the headerFilterFuncParams property

    if(rowValue){
        if(headerValue.start != ""){
            if(headerValue.end != ""){
                return rowValue >= headerValue.start && rowValue <= headerValue.end;
            }else{
                return rowValue >= headerValue.start;
            }
        }else{
            if(headerValue.end != ""){
                return rowValue <= headerValue.end;
            }
        }
    }

    return true; //must return a boolean, true if it passes the filter.
}
 //create Tabulator on DOM element with id "example-table"

const initColumnHeaders = [
    {title:"Favorites", field:"fav", formatter:"tickCross", editor: true, hozAlign: "center", editorParams:{
        trueValue: "TRUE",
        falseValue: "FALSE"
    }},
    {title:"Name", field:"name", headerFilter:true, headerFilterLiveFilter:false, frozen:true, width: 300},
    {title:"Density", field:"density"}, 
    {title:"Yield Strength", field: "tensile_strength_yield"}, 
    {title:"Ultimate Strength", field: "tensile_strength_ultimate"}, 
    {title:"Elastic Modulus", field: "modulus_of_elasticity"},
    {title: "Brinell Hardness", field: "hardness_brinell"},
    {title:"Specific Heat Capacity", field: "specific_heat_capacity"},
    {title:"Machinability", field:"machinability"},
]

let columnHeaders;
columnHeaders = initColumnHeaders;

columnHeaders = columnHeaders.map((colProp) => {
    if (colProp["field"] != "name" && colProp["field"] != "fav"){
        colProp.hozAlign = "center";
        colProp.sorter = "number";
        colProp.headerFilter = minMaxFilterEditor;
        colProp.headerFilterFunc = minMaxFilterFunction;
        colProp.headerFilterLiveFilter = false;
        colProp.resizable = false;
    }
    if ("true" != isAuthenticated){
        if (colProp["field"] != 'name' &&
            colProp["field"] != 'density' && 
            colProp["field"] != 'tensile_strength_yield' && 
            colProp["field"] != 'tensile_strength_ultimate' && 
            colProp["field"] != 'modulus_of_elasticity' &&
            colProp["field"] != 'fav'
        ){colProp.cssClass = "cell-blur";}
        if (colProp["field"] == "specific_heat_capacity"){
            colProp.cssClass = "cell-blur btn-anchor z-1";
        }
    }
    return colProp
});

let apiURL;
if ("true" == isAuthenticated){
    apiURL = "/api/tabulator"
}else{
    apiURL = "/api/data"
}

var table = new Tabulator("#table", {
    ajaxURL: apiURL,
    ajaxResponse: function(url, params, response) {
        // Assuming response is the entire API response object
        // var data = response.data || []; // Extract the "data" array
        return response.data || []; // Return the extracted array
    },
    layout: "fitColumns",
    pagination:true,
 	columns: columnHeaders,
});

//Reassign elements so button is fixed to element
if ("true" != isAuthenticated){
    window.onload = reAssignElement;
}

function reAssignElement(){
    const tableContent = document.querySelector(".tabulator-table"); 
    const tableWrapper = document.querySelector(".tabulator-tableholder")  
    const button = document.getElementById("anon-btn");
 
    tableWrapper.appendChild(button);
    tableContent.style.zIndex = 0;
    tableContent.style.position = "absolute";
    // centerColHeader.style.setProperty("overflow", "visible", "important");
    // centerColHeader.style.position = "relative";
    button.style.position = "absolute";
    // button.style.top = "200%";
    button.style.right = "15vw";
    // button.style.transform = "translate(-50%, 0)";
    button.style.zIndex = 10;
}
