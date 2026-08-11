const columns = [
    "checkbox",
    "jahr",
    "kw",
    "neue_kw",
    "kundenname",
    "vorgangsnummer",
    "vorgangstext",
    "artikelbeschreibung",
    "artikelnr",
    "neue_kw_nummerfeld",
    "lieferverzugs_grund_textfeld",
    "bestätigungs_button"
];

let insertedYears = new Set(); // To track inserted years
let selectedRow = null; // To track the currently selected row
const loader = document.getElementsByClassName('loader')[0];

function setSelectedRow(row) {
    selectedRow = row;
    document.querySelectorAll('.row_checkbox').forEach((checkbox) => {
        checkbox.checked = false;
    });
    document.querySelectorAll('.confirm_button').forEach((button) => {
        button.disabled = true;
    });
    document.querySelectorAll('.neue_kw_input').forEach((input) => {
        input.disabled = true;
    });
    document.querySelectorAll('.lieferverzugs_grund_input').forEach((input) => {
        input.disabled = true;
    });
    if (row) {
        const checkbox = document.getElementById(`checkbox_${row["vorgangsnummer"]}`);
        if (checkbox) checkbox.checked = true;
        const button = document.getElementById(`bestätigen_${row["vorgangsnummer"]}`);
        if (button) button.disabled = false;
        const neueKWInput = document.getElementById(`neue_kw_${row["vorgangsnummer"]}`);
        if (neueKWInput) neueKWInput.disabled = false;
        const lieferverzugsGrundInput = document.getElementById(`lieferverzugs_grund_${row["vorgangsnummer"]}`);
        if (lieferverzugsGrundInput) lieferverzugsGrundInput.disabled = false;
    }
}

async function getRows() {
    selectedRow = null;
    insertedYears.clear(); // Clear the set of inserted years before fetching new data
    const loader = document.getElementsByClassName('loader')[0];
    loader.style.display = 'block';
    const tableBody = document.getElementById('lieferungen_body');
    tableBody.innerHTML = '';
    let response;

    const currentDepartment = window.location.pathname.split('/').filter(Boolean).pop(); // Get the last part of the URL path
    console.log(`Fetching rows for department: ${currentDepartment}`);
    try {
        response = await fetch(`/rows/${currentDepartment}`, {
            method: 'GET',
        });
    }
    finally {
        loader.style.display = 'none'; // Hide the loader after data is loaded
    }
    if (!response.ok) throw new Error("Network response was not ok");

    // Prepare for incoming data
    const rows = await response.json();
    console.log(rows);
    rows.forEach((row) => {
        inserTableRow(row, rows);
    });
    setSelectedRow(null);
}

// Headers is a list of strings
function setTableHeader() {
    const table = document.getElementById('lieferungen');
    const thead = table.createTHead();
    const row = thead.insertRow();
    columns.forEach((header) => {
        const th = document.createElement('th');
        switch (header) {
            case "checkbox":
                th.textContent = "";
                break;
            case "bestätigungs_button":
                th.textContent = "";
                break;
            case "neue_kw_nummerfeld":
                th.textContent = "Neue KW";
                break;
            case "lieferverzugs_grund_textfeld":
                th.textContent = "Lieferverzugsgrund";
                break;
            case "kw":
                th.textContent = "KW";
                break;
            case "neue_kw":
                th.textContent = "Neue KW";
                break;
            default:
                th.textContent = header
                    .replace(/[-_]/g, ' ')
                    .replace(/(?:^|\s)\S/g, (char) => char.toUpperCase());
        }
        row.appendChild(th);
    });
}

function countRowspan(rows, currentYear) {
    let count = 0;
    rows.forEach((row) => {
        if (row["jahr"] === currentYear) {
            count++;
        }
    });
    return count;
}

function inserTableRow(rowData, rows) {
    const table = document.getElementById('lieferungen_body');
    const row = table.insertRow();
    for (let column of columns) {
        let cell;
        if (column !== "jahr") {
            cell = row.insertCell();
            cell.className = column; // Assign class name for styling
        }
        if (column === "checkbox") {
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `checkbox_${rowData["vorgangsnummer"]}`;
            checkbox.classList.add('row_checkbox');
            checkbox.addEventListener('change', (event) => {
                setSelectedRow(event.target.checked ? rowData : null);
            });
            cell.appendChild(checkbox);
        }
        else if (column === "bestätigungs_button") {
            const button = document.createElement('button');
            button.textContent = 'Abschicken';
            button.id = `bestätigen_${rowData["vorgangsnummer"]}`;
            button.classList.add('confirm_button');
            button.addEventListener('click', () => {
                // Handle button click event here
                sendLieferverzug(rowData);
            });
            cell.appendChild(button);
        }
        else if (column === "neue_kw_nummerfeld") {
            const input = document.createElement('input');
            input.type = 'number';
            input.id = `neue_kw_${rowData["vorgangsnummer"]}`;
            input.classList.add('neue_kw_input');
            input.style.width = '90%';
            input.value = '';
            cell.appendChild(input);
        }
        else if (column === "lieferverzugs_grund_textfeld") {
            const input = document.createElement('input');
            input.type = 'text';
            input.id = `lieferverzugs_grund_${rowData["vorgangsnummer"]}`;
            input.classList.add('lieferverzugs_grund_input');
            input.style.width = '90%';
            input.value = '';
            cell.appendChild(input);
        }
        else if (column === "jahr") {
            if (!insertedYears.has(rowData["jahr"])) {
                cell = row.insertCell();
                cell.className = column; // Assign class name for styling
                cell.innerHTML = "<span class='year_span'>" + rowData[column] + "</span>";
                console.log(`Setting rowspan for year: ${rowData["jahr"]}`);
                cell.rowSpan = countRowspan(rows, rowData["jahr"]); // Set rowspan for the "jahr" column
                insertedYears.add(rowData["jahr"]);
            }
        }
        else {
            cell.textContent = rowData[column] || '';
            if (column === "kw" || (column === "neue_kw" && rowData["neue_kw"] !== undefined)) { // Color se kalendarwoche Aarghrhghtghg
                const currentKW = getCurrentKW();
                const currentYear = new Date().getFullYear();
                if (currentYear > parseInt(rowData['jahr']) || (parseInt(rowData['jahr']) === currentYear && parseInt(rowData[column]) < currentKW)) {
                    cell.style.backgroundColor = 'red';
                }
                else if (parseInt(rowData[column]) === currentKW) {
                    cell.style.backgroundColor = 'yellow';
                }
                else if (parseInt(rowData[column]) > currentKW) {
                    cell.style.backgroundColor = '#4bc84b';
                }
            }
        }
    }
}

async function sendLieferverzug(rowData) {
    const neueKWInput = document.getElementById(`neue_kw_${rowData["vorgangsnummer"]}`);
    const lieferverzugsGrundInput = document.getElementById(`lieferverzugs_grund_${rowData["vorgangsnummer"]}`);
    const neueKW = neueKWInput ? neueKWInput.value : null;
    const lieferverzugsGrund = lieferverzugsGrundInput ? lieferverzugsGrundInput.value : null;
    const vorgangsnummer = rowData["vorgangsnummer"];
    const kommission = rowData["vorgangstext"];
    const artikelbeschreibung = rowData["artikelbeschreibung"];
    const email = rowData["email"] || null; // Get email from rowData if available

    const payload = {
        vorgangsnummer: vorgangsnummer,
        kommission: kommission,
        artikelbeschreibung: artikelbeschreibung,
        neue_kw: neueKW,
        lieferverzugs_grund: lieferverzugsGrund,
        email: email  // Include email if available
    };

    try {
        const response = await fetch('/verzug/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result.message);
        getRows(); // Refresh the table after sending data
    } catch (error) {
        console.error('Error sending lieferverzug data:', error);
    }
}

function getCurrentKW() { // Source: Gemini >:(
    const target = new Date();
    const dayNr = (target.getDay() + 6) % 7;
    target.setDate(target.getDate() - dayNr + 3);
    const firstThursday = new Date(target.getFullYear(), 0, 4);
    const firstThursdayDayNr = (firstThursday.getDay() + 6) % 7;
    firstThursday.setDate(firstThursday.getDate() - firstThursdayDayNr + 3);
    const millisecondsInWeek = 604800000;
    const kw = 1 + Math.round((target.getTime() - firstThursday.getTime()) / millisecondsInWeek);
    return kw;
}



setTableHeader();
getRows();