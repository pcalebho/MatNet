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

const anonTable = [ //Define Table Columns
{title:"Name", field:"name", headerFilter:true, headerFilterLiveFilter:false},
{title:"Density", field:"density", hozAlign:"left", sorter:"number", headerFilter:minMaxFilterEditor, headerFilterFunc:minMaxFilterFunction, headerFilterLiveFilter:false},
{title:"Yield Strength", field: "tensile_strength_yield", hozAlign:"left", sorter:"number", headerFilter:minMaxFilterEditor, headerFilterFunc:minMaxFilterFunction, headerFilterLiveFilter:false},
{title:"Ultimate Strength", field: "tensile_strength_ultimate", hozAlign:"left", sorter:"number", headerFilter:minMaxFilterEditor, headerFilterFunc:minMaxFilterFunction, headerFilterLiveFilter:false},
{title:"Elastic Modulus", field: "modulus_of_elasticity", hozAlign:"left", sorter:"number", headerFilter:minMaxFilterEditor, headerFilterFunc:minMaxFilterFunction, headerFilterLiveFilter:false},
];

const extraHeaders = [
    {title:"Specific Heat Capacity", field: "specific_heat_capacity", hozAlign:"left", sorter:"number", headerFilter:minMaxFilterEditor, headerFilterFunc:minMaxFilterFunction, headerFilterLiveFilter:false}
];

const authTable = anonTable.concat(extraHeaders)

let columnHeaders;
if ('true' == isAuthenticated){
    columnHeaders = authTable;
} else {
    columnHeaders = anonTable;
}

var table = new Tabulator("#table", {
    ajaxURL: "/api/tabulator",
    ajaxResponse: function(url, params, response) {
        // Assuming response is the entire API response object
        // var data = response.data || []; // Extract the "data" array
        return response.data || []; // Return the extracted array
    },
    pagination:true,
    // paginationSize:10,
    height: 700,
    // autoColumns: true,
    // autoColumnsDefinitions:function(definitions){
    //     //definitions - array of column definition objects

    //     definitions.forEach((column) => {
    //         column.headerFilter = true; // add header filter to every column
    //     });

    //     return definitions;
    // },
 	// height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
 	// data:tabledata, //assign data to table
 	// layout:"fitColumns", //fit columns to width of table (optional)
 	columns: columnHeaders
    // ajaxParams:{Name:"value1", Density:"value2"},
});
