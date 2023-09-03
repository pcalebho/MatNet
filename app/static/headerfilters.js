export let minMaxEditor = function(cell, onRendered, success, cancel, editorParams){
    let end;

    //create elements
    let container = document.createElement("div");
    let start = document.createElement("input");
    let filterContainer = document.createElement("div");

    //set attributes
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);    

    //set styles and classes
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";
    container.classList.add('custom-headerFilter');

    start.value = cell.getValue();

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    start.classList.add("min-input");
    end.classList.add("max-input");


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


    filterContainer.appendChild(start);
    filterContainer.appendChild(end);

    filterContainer.classList.add("filter-container")
    container.appendChild(filterContainer);

    return container;
}

export let minMaxTopsisEditor = function(cell, onRendered, success, cancel, editorParams){
    let end;

    //create elements
    let container = document.createElement("div");
    let minMaxSwitch = document.createElement("label");
    let start = document.createElement("input");
    let importance = document.createElement("input");
    let mcdmContainer = document.createElement("div");
    let filterContainer = document.createElement("div");

    //set attributes
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);    
    importance.setAttribute("type","range");
    importance.setAttribute("min",0);
    importance.setAttribute("max",10); 
    importance.setAttribute("step",1); 
    importance.setAttribute("value",0);
    importance.classList.add("form-range")

    //set styles and classes
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";
    container.classList.add('custom-headerFilter');

    start.value = cell.getValue();

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    minMaxSwitch.classList.add("minMaxToggle");

    const toggle = document.createElement("input");
    toggle.setAttribute("type","checkbox");

    const toggleLabel = document.createElement("span");
    toggleLabel.classList.add("labels");
    toggleLabel.setAttribute("data-on","MIN");
    toggleLabel.setAttribute("data-off","MAX");

    start.classList.add("min-input");
    end.classList.add("max-input");


    function buildValues(){ 
        success({
            start:start.value,
            end:end.value,
            importance: importance.value,
            objective: toggle.checked
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

    minMaxSwitch.appendChild(toggle);
    minMaxSwitch.appendChild(toggleLabel);

    filterContainer.appendChild(start);
    filterContainer.appendChild(end);
    mcdmContainer.appendChild(importance);
    mcdmContainer.appendChild(minMaxSwitch);

    filterContainer.classList.add("filter-container")
    mcdmContainer.classList.add("mcdm-container")
    container.appendChild(mcdmContainer);
    container.appendChild(filterContainer);

    return container;
}

//custom max min filter function
export function minMaxTopsisFunction(headerValue, rowValue, rowData, filterParams){
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

//custom max min filter function
export function minMaxFunction(headerValue, rowValue, rowData, filterParams){
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