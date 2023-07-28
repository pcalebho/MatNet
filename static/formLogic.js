const app = Vue.createApp({
    data() {
        return {
            value0: 0,
            value1: 0,
            value2: 0,
            value3: 0,
            value4: 0,
            isSliding: false, // To track if a slider is being actively dragged
        };
    },
    methods: {
        handleSliderChange() {
            if (!this.isSliding) {
                // Make the POST request here
                this.makePostRequest();
            }
        },
        makePostRequest() {
            // Your POST request logic here
            fetch("/api/data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ value: [this.value0, this.value1, this.value2, this.value3, this.value4] }),
            })
            .then((response) => response.json())
            .then((data) => {
                console.log("POST request successful!", data);
                // Do something with the response if needed
            })
            .catch((error) => {
                console.error("Error sending POST request:", error);
            });
        },
    },
    delimiters: ['[[',']]']
});

app.mount('#criterion-forms')