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