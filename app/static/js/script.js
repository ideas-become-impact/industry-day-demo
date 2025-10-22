const graph_1 = document.getElementById("graph_1")
const graph_2 = document.getElementById("graph_2")

const button_1 = document.getElementById("button_1")
const button_2 = document.getElementById("button_2")

const data_colors = {
    backgroundColor: "#dfad8a",
    borderColor: "rgb(255, 0, 0)",
    borderWidth: 5,
    radius: 0,
}

let xhr = new XMLHttpRequest();

const options = {
    maintainAspectRatio: false,
    scales: {
        x: {
            type: 'linear'
        },
        y: {
            type: 'linear'
        }
    }
}

const charts = {}
const data = fetch("/data_route").then(data => data.json()).then(data => {
    const plottable_data = {
        datasets: [{
            ...data_colors,
            data: data
        }]
    }

    const config = {
        type: 'line',
        data: plottable_data,
        options: options
    };

    const myChart = new Chart(
        document.getElementById('graph_1_image'),
        config,
    );

    charts.one = myChart;
});


const data2 = fetch("/jumping-data-route").then(data => data.json()).then(data => {
    const plottable_data = {
        datasets: [{
            ...data_colors,
            data: data
        }]
    }

    const config = {
        type: 'line',
        data: plottable_data,
        options: options
    };

    const myChart_2 = new Chart(
        document.getElementById('graph_2_image'),
        config
    );

    charts.two = myChart_2;

});

function update_chart(chart_number) {
    switch (chart_number) {
        case 1: fetch("/data_route").then(data => data.json()).then(new_data => {
            charts.one.data.datasets[0].data = new_data;
            charts.one.update();
        });
        case 2: fetch("/jumping-data-route").then(data => data.json()).then(new_data => {
            charts.two.data.datasets[0].data = new_data;
            charts.two.update();
        });
    }
}

function turnOnGraph(caller) {
    id = caller.id;

    on_req = { "push_data": true }
    fetch("/recv-output", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(on_req)
    });
    if (id == "button_1") {
        caller.parentNode.style.flexGrow = 2;
        caller.parentNode.style.flexShrink = 0;

        graph_2.parentNode.style.flexShrink = 2;
        graph_2.parentNode.style.flexGrow = 0;

        graph_1.style.display = "flex";
        graph_2.style.display = "none";

    } else {
        caller.parentNode.style.flexGrow = 2;
        caller.parentNode.style.flexShrink = 0;

        graph_1.parentNode.style.flexShrink = 2;
        graph_1.parentNode.style.flexGrow = 0;

        graph_1.style.display = "none";
        graph_2.style.display = "flex";
    }

    if (graph_1.style.display == "flex") {
        button_1.style.display = "none";
        button_2.style.display = "flex";
        update_chart(1);
    }

    if (graph_2.style.display == "flex") {
        button_2.style.display = "none";
        button_1.style.display = "flex";
        update_chart(2);
    }
}

function turnOffGraph(caller) {
    all_children = caller.parentNode.children;

    off_req = { "push_data": false }
    fetch("/recv-output", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(off_req)
    });
    for (const child of all_children) {
        if (child.classList.contains("collection")) {
            child.style.display = "flex";
        }

        if (child.classList.contains("graph")) {
            child.style.display = "none";
            console.log("happened! x3");
            if (child.id == "graph_1") {
                console.log("did hapepn!");
                charts.one.config.data.datasets[0].data = [0, 0, 0, 0, 0];
                charts.one.update();
            } else if (child.id == "graph_2") {
                charts.two.config.data.datasets[0].data = [0, 0, 0, 0, 0];
                charts.two.update();
            }
        }
    }
}