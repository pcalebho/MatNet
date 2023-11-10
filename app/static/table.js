import * as hf from '/static/headerfilters.js'
import * as pop from '/static/popup.js'

let colHeaderFilter = hf.minMaxEditor;
const topsisSwitchDiv = document.getElementById("TOPSIS");
const topsisSwitch = document.querySelector(".form-check-input");
const dataChoiceRadio = document.getElementById("dataChoiceRadio")

const initDataState = document.querySelector('input[name="btnradio"]:checked').value

const baseColumnHeaders = [
    {title:"Name", field:"name", headerFilter:true, headerFilterLiveFilter:false, headerFilterPlaceholder:"Find a material...", frozen:true, width: 300},
    {title:"Yield Strength (MPa)", field: "tensile_strength_yield", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true, 
        headerTooltip: "Maximum stress a material can tolerate before it begins to deform plastically"
    }, 
    {title:"Ultimate Strength (MPa)", field: "tensile_strength_ultimate", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Maximum stress that a material can withstand before it breaks or weakens"
    },
]

const genColumnHeaders = [
    {title:"Density (g/cm^3)", field:"density", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Ratio of mass to volume. Mass/Volume."
    }, 
    {title:"Elastic Modulus (GPa)", field: "modulus_of_elasticity", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Material's resistance to being deformed elastically (i.e., non-permanently) when a stress is applied to it"
    },
    {title: "Brinell Hardness", field: "hardness_brinell", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Measure of a metal or alloy's resistance to permanent indentation deformation"
    },
    {title:"Specific Heat Capacity (J/g-°C)", field: "specific_heat_capacity", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true, 
        headerTooltip: "Measure on amount of heat needed to raise temperature of material"
    },
    {title:"Machinability", field:"machinability", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Reference machinability is AISI 1212 Steel at 100%. Larger number means higher machinability."
    },
]

const fatigueColumnHeaders = [
    {title:"Product Form", field: "product_form",  headerFilter:true, headerFilterLiveFilter:false, headerFilterPlaceholder:"Find form...",  headerWordWrap:true,
        headerTooltip: "Form of material that was tested."
    },
    {title:"Stress Concentration Factor (Kt)", field: "k_value", sorter: "number", hozAlign: "center", headerFilter: colHeaderFilter, headerFilterLiveFilter: false,  headerWordWrap:true,
        headerTooltip: "Measures stress concentration in a mechanical part. It's the ratio of the highest stress to a reference stress. A value of 1 would be unnotched."
    },
    {title:"Fatigue Curves", field: "id", hozAlign:"center", headerSort: false, formatter:"link", formatterParams:{
        labelField:"link_label",
        urlPrefix:"/fatigue/",
        target:"_blank",
    }},
]

let columnHeaders = baseColumnHeaders.concat(genColumnHeaders)
if (initDataState == "fatigue"){
    columnHeaders = baseColumnHeaders.concat(fatigueColumnHeaders)
    topsisSwitch.setAttribute("disabled", "");    
} 


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
    progressiveLoad:"load",
 	columns: columnHeaders,
    rowClickPopup:pop.rowPopupFormatter,
    ajaxParams: function(){
        return {source: document.querySelector('input[name="btnradio"]:checked').value}
    },
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
    },
    dataLoaderLoading: "<div class='spinner-border text-primary' role='status' style='display: inline-block;'></div><span class='sr-only'>Loading...</span>",
    layoutColumnsOnNewData:true,
});

dataChoiceRadio.addEventListener('change', () => {
    let dataState = document.querySelector('input[name="btnradio"]:checked').value;             //value of the datasheet radio
    let topsisSwitchState = document.querySelector('.form-check-input').checked;

    table.clearData()
    table.setData()
    .then(function(){
        if (dataState == "fatigue"){
            for (const gch of genColumnHeaders){
                table.deleteColumn(gch.field)
            }
            for (const fch of fatigueColumnHeaders){
                table.addColumn(fch)
            }
            for (const bch of baseColumnHeaders){
                if (bch.field != 'name'){
                    table.updateColumnDefinition(bch.field, {headerFilter: hf.minMaxEditor})
                }
            }
            topsisSwitch.setAttribute("disabled", "");   
            if (topsisSwitchState){
                table.deleteColumn("score")
            }
        } else {
            for (const gch of genColumnHeaders) {
                table.addColumn(gch)
            }
            for (const fch of fatigueColumnHeaders){
                table.deleteColumn(fch.field)
            }
            if (topsisSwitchState){
                table.addColumn({title:"Score", field:"score", width: 100}, true, "name");
                table.updateColumnDefinition("density", {headerFilter: hf.minMaxTopsisEditor})
                table.updateColumnDefinition("tensile_strength_yield", {headerFilter: hf.minMaxTopsisEditor})
                table.updateColumnDefinition("tensile_strength_ultimate", {headerFilter: hf.minMaxTopsisEditor})
                table.updateColumnDefinition("modulus_of_elasticity", {headerFilter:hf.minMaxTopsisEditor})
                table.updateColumnDefinition("specific_heat_capacity", {headerFilter: hf.minMaxTopsisEditor})
                table.updateColumnDefinition("machinability", {headerFilter: hf.minMaxTopsisEditor})
                table.updateColumnDefinition("hardness_brinell", {headerFilter: hf.minMaxTopsisEditor})
            }
            topsisSwitch.removeAttribute("disabled");    
        }
    })
    .catch(function(error){
        console.log(error)
    });
})

topsisSwitchDiv.addEventListener('change', () => {
    const check = document.querySelector('input[name="btnradio"]:checked').value
    if (check == "fatigue"){
        return
    }

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
