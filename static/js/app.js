document.getElementById("generate-code-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const duration = document.getElementById("duration").value;

    const response = await fetch("/generate_code", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `duration=${encodeURIComponent(duration)}`
    });

    const result = await response.json();
    document.getElementById("code-result").innerText = 
        `Generated Code: ${result.code}, Expires At: ${result.expires_at}`;
});
