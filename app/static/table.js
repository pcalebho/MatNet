import * as hf from '/static/headerfilters.js'
import * as pop from '/static/popup.js'

let colHeaderFilter = hf.minMaxEditor;
const topsisSwitch = document.getElementById("TOPSIS");

const initColumnHeaders = [
    {formatter:"rowSelection", titleFormatter:"rowSelection", hozAlign:"center", headerSort:false, width: 50, cellClick:function(e, cell){
        cell.getRow().toggleSelect();
    }},
    // {title:"Favorites", field:"fav", width: 50, editor: "tickCross", hozAlign: "center", editorParams:{
    //     trueValue: "★",
    //     falseValue: "☆"
    // }},
    {title:"Name", field:"name", headerFilter:true, headerFilterLiveFilter:false, headerFilterPlaceholder:"Find a material...", frozen:true, width: 300},
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
        colProp.headerFilter = colHeaderFilter;
        // colProp.headerFilterFunc = hf.minMaxTopsisFunction;
        colProp.headerFilterLiveFilter = false;
        colProp.resizable = false;
    }
    if ("true" != isAuthenticated){
        if (colProp["field"] == 'hardness_brinell' ||
            colProp["field"] == 'specific_heat_capacity' ||
            colProp["field"] == 'machinability'
        ){colProp.cssClass = "cell-blur";}
        if (colProp["field"] == "specific_heat_capacity"){
            colProp.cssClass = "cell-blur btn-anchor z-1";
        }
    }
    return colProp
});


var table = new Tabulator("#table", {
    ajaxURL: '/api/tabulator',
    ajaxResponse: function(url, params, response) {
        // Assuming response is the entire API response object
        // var data = response.data || []; // Extract the "data" array
        return response.data || []; // Return the extracted array
    },
    filterMode: "remote",
    layout: "fitColumns",
    pagination:true,
 	columns: columnHeaders,
    rowClickPopup:pop.rowPopupFormatter,
    langs:{
    "en-gb":{
        "headerFilters":{
            "columns":{
                "Name":"filter name...", //replace default header filter text for column name
            }
        }
    }
    },
    ajaxURLGenerator:function(url, config, params){
        //url - the url from the ajaxURL property or setData function
        //config - the request config object from the ajaxConfig property
        //params - the params object from the ajaxParams property, this will also include any pagination, filter and sorting properties based on table setup

        //return request url
        return url + "/params/" + encodeURI(JSON.stringify(params)); //encode parameters as a json object
    },
    ajaxConfig:{
        // method:"POST", //set request type to Position
        headers: {
            "Content-type": 'application/json; charset=utf-8', //set specific content type
        },
    }
});

topsisSwitch.addEventListener('change', () => {
    if (colHeaderFilter === hf.minMaxEditor){
        colHeaderFilter = hf.minMaxTopsisEditor;
        table.addColumn({title:"Score", field:"score", width: 100}, true, "name");
    } else {
        colHeaderFilter = hf.minMaxEditor;
        table.deleteColumn("score")
    }

    table.updateColumnDefinition("density", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("tensile_strength_yield", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("tensile_strength_ultimate", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("modulus_of_elasticity", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("specific_heat_capacity", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("machinability", {headerFilter: colHeaderFilter})
    table.updateColumnDefinition("hardness_brinell", {headerFilter: colHeaderFilter})
});

//Reassign elements so button is fixed to element
table.on("tableBuilt", reAssignElement);

function reAssignElement(){
    const tableContent = document.querySelector(".tabulator-table"); 
    const colAnchor = document.querySelector(".btn-anchor.tabulator-col");
    const button = document.getElementById("anon-btn");
    const footer = document.querySelector(".tabulator-footer");

    let anchorRect = colAnchor.getBoundingClientRect();
    let footerRect = footer.getBoundingClientRect();

    let xPos = anchorRect.x+anchorRect.width/2;
    let yPos = (footerRect.top-anchorRect.bottom)/2;
 
    tableContent.style.zIndex = 0;
    button.style.position = "fixed";
    button.style.top = yPos+"px";
    button.style.left = xPos+"px";
    button.style.transform = "translate(-50%, 50%)";    
    button.style.zIndex = 10;
}
