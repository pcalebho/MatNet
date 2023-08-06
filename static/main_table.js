const updateUrl = (prev, query) => {
    return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
};

const table = new gridjs.Grid({
    columns: [
        { id: 'name', name: 'Name', width: '8%', sort: false},
        { id: 'density', width: '7%', name: 'Density' },
        { id: 'modulus_of_elasticity',width: '10%', name: 'Elastic Modulus' },
        { id: 'tensile_strength_yield',width: '10%', name: 'Yield Strength'},
        { id: 'tensile_strength_ultimate',width: '10%', name: 'Ultimate Strength'},
        { id: 'hardness_brinell', width: '10%',name: 'Brinell Hardness' },
        { id: 'specific_heat_capacity', width: '10%',name: 'Specific Heat Capacity' },
        { id: 'cost', width: '8%',name: '*Cost' },
        { id: 'machinability', width: '8%',name: 'Machineability'},
        { id: 'Rank', name: '**Rank'}
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
        debounceTimeout: 1000
    },
    sort: {
        enabled: true,
        multiColumn: true,
        server: {
            url: (prev, columns) => {
                const columnIds = [
                    'name',
                    'density',
                    'modulus_of_elasticity',
                    'tensile_strength_yield',
                    'tensile_strength_ultimate',
                    'hardness_brinell',
                    'specific_heat_capacity',
                    'cost',
                    'machinability',
                    'Score_rank'
                ];
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
    width: '90%',
    style: {
        container: {
            'margin-top': '1em',
            'margin-left': '5%',
            'margin-right': '5%'
        },
        table: {
            'font-size': '11px',
            'width': '100%'
        },
        th: {
            'font-size': '1em',
            'text-align': 'left',
            'padding': '1em'
        },
        td: {
            'text-align': 'center',
            'padding': '5px'
        }
    }
})

table.render(document.getElementById('table'));

// const searchInput = document.getElementById('searchInput');
// let searchString = '';

// searchInput.addEventListener('keypress', (event) => {
//     if (event.key === 'Enter') {
//         searchString = event.target.value.trim();
//         table.search(searchString);
//     }
// });


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
    for (let i = 0; i < 8; i++) {
        importance = document.getElementById('sliderRange-'+i).value;
        objective = document.getElementById('objective-'+i).value;
        min_value = document.getElementById('minValue-'+i).value;
        max_value = document.getElementById('maxValue-'+i).value;
        property = document.getElementById('prop-'+i).innerHTML;

        if (min_value != "" && max_value != "" && +min_value > +max_value ){
            min_value = "";
            max_value = "";
        }

        formEntry = {importance: +importance, objective: +objective, min: min_value, max: max_value};
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