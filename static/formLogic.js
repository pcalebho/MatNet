const app = Vue.createApp({
    data() {
        return {
            value0: 0,
            value1: 0,
            value2: 0,
            value3: 0,
            value4: 0,
            value5: 0,
            value6: 0,
            value7: 0
            // isSliding: false, // To track if a slider is being actively dragged
        };
    },
});

app.config.compilerOptions.delimiters = ['[[',']]']
app.mount('form')