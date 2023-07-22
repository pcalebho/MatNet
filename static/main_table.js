const updateUrl = (prev, query) => {
    return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
};

new gridjs.Grid({
columns: [
    { id: 'name', name: 'Name', width: '20%', sort: false},
    { id: 'elastic_mod', name: 'Modulus of Elasticity' },
    { id: 'yield_strength', name: 'Yield Strength'},
    { id: 'ult_strength', name: 'Ultimate Strength'},
    { id: 'cost', name: 'Cost'},
    { id: 'machineability', name: 'Machineability'}
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
        const columnIds = ['name', 'elastic_mod', 'yield_strength', 'ult_strength', 'cost', 'machineability'];
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
}).render(document.getElementById('table'));