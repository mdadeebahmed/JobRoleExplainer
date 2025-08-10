async function explainJobRole() {
    const jobTitle = document.getElementById("jobTitle").value;
    const resultBox = document.getElementById("result");

    if (!jobTitle.trim()) {
        resultBox.value = "Please enter a job title.";
        return;
    }

    resultBox.value = "Loading...";

    try {
        const response = await fetch("/explain_job_role", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_title: jobTitle })
        });

        const data = await response.json();
        resultBox.value = data.result_markdown || "No explanation available.";
    } catch (error) {
        resultBox.value = "Error: " + error;
    }
}
