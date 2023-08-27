var minMaxFilterEditor = function(cell, onRendered, success, cancel, editorParams){
    var end;

    var container = document.createElement("span");

    //create and style inputs
    var start = document.createElement("input");
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";

    start.value = cell.getValue();

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

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);


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
    if (colProp["field"] != "name"){
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
            colProp["field"] != 'modulus_of_elasticity'
        ){colProp.cssClass = "cell-blur"}
    }
    return colProp
});


var table = new Tabulator("#table", {
    ajaxURL: "/api/tabulator",
    ajaxResponse: function(url, params, response) {
        // Assuming response is the entire API response object
        // var data = response.data || []; // Extract the "data" array
        return response.data || []; // Return the extracted array
    },
    layout: "fitColumns",
    pagination:true,
 	columns: columnHeaders,
});
