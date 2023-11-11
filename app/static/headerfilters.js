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
    importance.setAttribute("type","number");
    importance.setAttribute("min",0);
    importance.setAttribute("max",10); 
    importance.setAttribute("placeholder","weight");
    importance.setAttribute("style", "font-size: .8rem")
    importance.classList.add("form-control")

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

    importance.addEventListener("change", buildValues);
    importance.addEventListener("blur", buildValues);
    importance.addEventListener("keydown", keypress);

    minMaxSwitch.addEventListener("change", buildValues);

    importance.addEventListener('input', e=>{
        const el = e.target || e
      
        if(el.type == "number" && el.max && el.min ){
          let value = parseInt(el.value)
          el.value = value // for 000 like input cleanup to 0
          let max = parseInt(el.max)
          let min = parseInt(el.min)
          if ( value > max ) el.value = el.max
          if ( value < min ) el.value = el.min
        }
    });


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
async function getFatigueCategories() {
    const response = await fetch('/api/fatigueCategories');
    return await response.json();
}

const categories = await getFatigueCategories()
categories.unshift("")


export let dropDownFilter = function(cell, onRendered, success, cancel, editorParams){
    //create elements
    let container = document.createElement("div");
    let dropdown = document.createElement("select");


    //set attributes
    dropdown.setAttribute("name", "category")

    //set styles and classes
    container.classList.add('custom-headerFilter');
    dropdown.classList.add("form-select");

    dropdown.value = cell.getValue();

    for (let category of categories){
        let option = document.createElement("option");
        option.setAttribute("value", category)
        option.textContent = category
        dropdown.appendChild(option)
    }

    function buildValues(){ 
        success({
            dropdownValue:dropdown.value,
        });
    }


    dropdown.addEventListener("change", buildValues);


    container.appendChild(dropdown);

    return container;
}