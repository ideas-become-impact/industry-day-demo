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

let start_time = performance.now()

let total_stand_data = []
let total_exercise_data = []

const options = {
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'linear'
      },
      y: {
        type: 'linear'
      }
    },
    plugins: {
        legend: {
            display: false
        }
    }
}

const charts = {}

const plottable_data1 = {
    datasets: [{
        ...data_colors,
        data: total_stand_data
    }]
}

const config1 = {
    type: 'line',
    data: plottable_data1,
    options: options
};

const chart1 = new Chart(
    document.getElementById('graph_1_image'),
    config1,
);

charts.one = chart1;

const plottable_data2 = {
    datasets: [{
        ...data_colors,
        data: total_exercise_data
    }]
}

const config2 = {
    type: 'line',
    data: plottable_data2,
    options: options
};

const chart2 = new Chart(
    document.getElementById('graph_2_image'),
    config2
);

charts.two = chart2;

// const data = fetch("/data_route").then(data => data.json()).then(data => {

// });


// const data2 = fetch("/jumping-data-route").then(data => data.json()).then(data => {


// });

function update_chart(chart_number) {
    elapsed_time = performance.now() / 1000.0 - start_time;

    switch (chart_number) {
        case 1:
            time_addition = {"elapsed_time": elapsed_time}
            fetch("/data-route", {
                method: "POST",
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(time_addition)
            }).then(data => data.json()).then(new_data => {
                charts.one.data.datasets[0].data = total_stand_data.concat(new_data);
                total_stand_data = total_stand_data.concat(new_data);
                charts.one.update();
            });
            break;
        case 2:
            time_addition = {"elapsed_time": elapsed_time}
            fetch("/jumping-data-route", {
                method: "POST",
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(time_addition)
            }).then(data => data.json()).then(new_data => {
                charts.two.data.datasets[0].data = total_exercise_data.concat(new_data);
                total_exercise_data = total_exercise_data.concat(new_data);
                charts.two.update(); 
            });
            break;
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
        total_exercise_data = []
        
    } else {
        caller.parentNode.style.flexGrow = 2;
        caller.parentNode.style.flexShrink = 0;

        graph_1.parentNode.style.flexShrink = 2;
        graph_1.parentNode.style.flexGrow = 0;

        graph_1.style.display = "none";
        total_stand_data = []
        graph_2.style.display = "flex";
    }

    if (graph_1.style.display == "flex") {
        button_1.style.display = "none";
        button_2.style.display = "flex";
        start_time = performance.now() / 1000.0;

        update_chart(1);
    }

    if (graph_2.style.display == "flex") {
        button_2.style.display = "none";
        button_1.style.display = "flex";
        start_time = performance.now() / 1000.0;

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
            if (child.id == "graph_1") {
                charts.one.config.data.datasets[0].data = [];
                total_stand_data = []
                start_time = performance.now() / 1000.0;
                charts.one.update();
            } else if (child.id == "graph_2") {
                charts.two.config.data.datasets[0].data = [];
                total_exercise_data = []
                start_time = performance.now() / 1000.0;
                charts.two.update();
            }
        }
    }
}




async function updateExerciseStatus() {
    try {
        const url = (window && window.EXERCISE_URL) ? window.EXERCISE_URL : "/api/test";
        const response = await fetch(url);
        const data = await response.json();
        const value = data.exercise;

        const statusText = document.getElementById("exercise-status");
        const imgEl = document.getElementById("exercise-image");

        if (value === 0) {
            statusText.textContent = "You are standing.";
            if (imgEl) {
                imgEl.src = (window && window.STAND_URL) ? window.STAND_URL : "/static/images/stand.svg";
                imgEl.alt = "Standing";
                imgEl.style.display = "block";
            }
        } else if (value === 1) {
            statusText.textContent = "You are jumping!";
            if (imgEl) {
                imgEl.src = (window && window.JUMP_URL) ? window.JUMP_URL : "/static/images/jumping_jacks.svg";
                imgEl.alt = "Jumping Jacks";
                imgEl.style.display = "block";
            }
        } else {
            statusText.textContent = "Unknown state.";
            if (imgEl) {
                imgEl.removeAttribute("src");
                imgEl.style.display = "none";
            }
        }
    } catch (err) {
        console.error("Error fetching exercise:", err);
        document.getElementById("exercise-status").textContent = "Error loading status.";
        const imgEl = document.getElementById("exercise-image");
        if (imgEl) imgEl.style.display = "none";
    }
}

setInterval(updateExerciseStatus, 2000);

document.addEventListener("DOMContentLoaded", updateExerciseStatus);
} 

setInterval(() => {
    if (performance.now() / 1000.0 - start_time < 30) {
        if (graph_1.style.display == "flex" && graph_2.style.display != "flex") {
            update_chart(1);
        } else if (graph_1.style.display != "flex" && graph_2.style.display == "flex") {
            update_chart(2);
        } else if (graph_1.style.display != "flex" && graph_2.style.display != "flex") {
            //
        } else {
            //
        }
    }
}, 1000);

