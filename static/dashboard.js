async function load() {
    const res = await fetch('/api/logs');
    const data = await res.json();

    let html = "";
    let attack = 0, success = 0, failed = 0;

    data.forEach(log => {

        let color = "white";
        if (log[2] == "CRITICAL") color = "red";
        else if (log[2] == "WARNING") color = "orange";

        html += `<tr style="color:${color}">
            <td>${log[0]}</td>
            <td>${log[1]}</td>
            <td>${log[2]}</td>
            <td>${log[3]}</td>
        </tr>`;

        if (log[1].includes("Injection") || log[1].includes("Force")) attack++;
        else if (log[1].includes("Success")) success++;
        else failed++;
    });

    document.getElementById("logs").innerHTML = html;

    new Chart(document.getElementById("chart"), {
        type: "bar",
        data: {
            labels: ["Attacks", "Success", "Failed"],
            datasets: [{
                data: [attack, success, failed]
            }]
        }
    });
}

setInterval(load, 2000);