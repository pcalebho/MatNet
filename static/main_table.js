const updateUrl = (prev, query) => {
    return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
};

const table = new gridjs.Grid({
columns: [
    { id: 'name', name: 'Name', width: '20%', sort: false},
    { id: 'elastic_mod', name: 'Modulus of Elasticity' },
    { id: 'yield_strength', name: 'Yield Strength'},
    { id: 'ult_strength', name: 'Ultimate Strength'},
    { id: 'cost', name: 'Cost'},
    { id: 'machineability', name: 'Machineability'},
    { id: 'Rank', name: 'Rank'}
],
server: {
    url: '/api/data',
    then: results => results.data,
    total: results => results.total,
},
search: {
    enabled: true,
    server: {
    url: (prev, search) => {
        return updateUrl(prev, {search});
    },
    },
},
sort: {
    enabled: true,
    multiColumn: true,
    server: {
    url: (prev, columns) => {
        const columnIds = ['name', 'elastic_mod', 'yield_strength', 'ult_strength', 'cost', 'machineability', 'Rank'];
        const sort = columns.map(col => (col.direction === 1 ? '+' : '-') + columnIds[col.index]);
        return updateUrl(prev, {sort});
    },
    },
},
pagination: {
    enabled: true,
    server: {
    url: (prev, page, limit) => {
        return updateUrl(prev, {start: page * limit, length: limit});
    },
    },
},
})

table.render(document.getElementById('table'));


// Function to handle form submission
async function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission
  
    // Collect the form data
    let importance;
    let objective;
    let min_value;
    let max_value;
    let formEntry = {};
    const formData = {};
    for (let i = 0; i < 2; i++) {
        importance = document.getElementById('sliderRange-'+i).value;
        objective = document.getElementById('objective-'+i).value;
        min_value = document.getElementById('minValue-'+i).value;
        max_value = document.getElementById('maxValue-'+i).value;
        property = document.getElementById('prop-'+i).innerHTML;

        if (min_value != "" && max_value != "" && +min_value > +max_value ){
            min_value = "";
            max_value = "";
        }

        formEntry = {importance: +importance, objective: objective, min: min_value, max: max_value};
        formData[property] = formEntry;
    }

    try {
        // Send the form data to the server using a POST request
        const response = await fetch('/api/data', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        
        if (response.ok) {
            // If the POST request is successful, reload the Grid.js table to fetch updated data
            const dataResponse = await response.json();
            console.log(dataResponse)
            table.forceRender();
        } else {
            console.error('POST request failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error making POST request:', error);
    }
}
  
// Attach the event listener to the form's submit event
const form = document.getElementById('form');
form.addEventListener('submit', handleSubmit);