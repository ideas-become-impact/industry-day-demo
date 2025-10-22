const graph_1 = document.getElementById("graph_1")
const graph_2 = document.getElementById("graph_2")

const button_1 = document.getElementById("button_1")
const button_2 = document.getElementById("button_2")

const labels = [' hello ', 'a', 'b', 'c', 'd']
const data = fetch("/data_route")
    .then(data => data.json())
    .then(data => {
        const plottable_data = {
            labels: labels,
            datasets: [{
                label: "waow",
                backgroundColor: "#dfad8a",
                borderColor: "rgb(255, 0, 0)",
                data: data
            }]
        }

        const config = {
            type: 'line',
            data: data,
            options: { maintainAspectRatio: false }
        };

        const myChart = new Chart(
            document.getElementById('graph_1_image'),
            plottable_data,
        );

        const myChart_2 = new Chart(
            document.getElementById('graph_2_image'),
            plottable_data,
        );
    })
    .catch(err => console.error(err))



function turnOnGraph(caller) {
    id = caller.id;
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
    }

    if (graph_2.style.display == "flex") {
        button_2.style.display = "none";
        button_1.style.display = "flex";
    }
}


function goToTest() {
    window.location.href = "test.html";
}

function goToHome() {
    window.location.href = "home.html";
}

