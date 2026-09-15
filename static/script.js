const form = document.getElementById("troubleshootForm");

const resultBox = document.getElementById("result");
const resultText = document.getElementById("resultText");
const resultTitle = document.getElementById("resultTitle");
const confidence = document.getElementById("confidence");
const sourceList = document.getElementById("sourceList");



form.addEventListener("submit", async function (event) {

    event.preventDefault();


    const equipment =
        document.getElementById("equipment").value;

    const problem =
        document.getElementById("problem").value.trim();


    if (!problem) {

        alert("Please describe the problem first.");

        return;
    }


    const button =
        document.querySelector(".analyze-button");


    button.disabled = true;

    button.innerHTML = `
        Analyzing...
        <span>◌</span>
    `;


    resultBox.classList.add("hidden");


    try {

        const response = await fetch("/api/troubleshoot", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                equipment: equipment,
                problem: problem
            })

        });


        if (!response.ok) {

            throw new Error(
                "Backend request failed."
            );

        }


        const data = await response.json();


        resultTitle.textContent =
            data.title || "Analysis complete";


        resultText.textContent =
            data.answer || "No answer received.";


        confidence.textContent =
            data.confidence || "--";


        sourceList.textContent =
            data.sources?.join(" • ") || "No sources returned";


        resultBox.classList.remove("hidden");


        resultBox.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        console.error(error);

        resultTitle.textContent =
            "NODEFIX couldn't complete the analysis";


        resultText.textContent =
            "The backend could not process your request. Please check that the Flask server is running.";


        confidence.textContent = "--";

        sourceList.textContent =
            "Backend unavailable";


        resultBox.classList.remove("hidden");

    } finally {

        button.disabled = false;

        button.innerHTML = `
            Analyze with NODEFIX
            <span>→</span>
        `;

    }

});