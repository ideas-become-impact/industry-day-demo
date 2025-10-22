
let prediction_state = false;

const statusText = document.getElementById("exercise-status");
const imgEl = document.getElementById("exercise-image");

async function updateExerciseStatus() {
    try {
        const url = (window && window.EXERCISE_URL) ? window.EXERCISE_URL : "/api/test";
        const response = await fetch(url);
        const data = await response.json();
        const value = data.exercise;

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

async function can_predict() {
    let is_available = true;

    await fetch("/train", {
                method: "POST",
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({"is_available": is_available})
            }).then(data => data.json()).then(data => {
        if (data.ready) {
            prediction_state = true;
        }
    });

    if (prediction_state) {
        imgEl.style.display = "block";
    }
}

async function predict() {
    const data = await fetch("/arduino-read-data").then(data => data.json()).then(data => data["data"]);

    const prediction = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"data": data})
    }).then(data => data.json()).then(data => data["state"]);

    return prediction
}

setInterval(updateExerciseStatus, 2000);

document.addEventListener("DOMContentLoaded", updateExerciseStatus);