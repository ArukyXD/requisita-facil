function recalc() {
    const goal = Number(document.getElementById("production_goal")?.value || 0);

    document.querySelectorAll("tbody tr").forEach((row) => {
        const consumption = Number(row.querySelector(".consumption")?.innerText || 0);
        const available = Number(row.querySelector(".available")?.value || 0);
        const needed = goal * consumption;
        const request = Math.max(needed - available, 0);

        row.querySelector(".needed").innerText = needed.toFixed(2);
        row.querySelector(".request").innerText = request.toFixed(2);
    });
}

document.querySelectorAll("input").forEach((input) => input.addEventListener("input", recalc));
recalc();
