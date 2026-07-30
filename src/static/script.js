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
    "neue_kw-nummerfeld",
    "lieferverzugs-grund-textfeld",
    "bestätigungs-button"
];

let insertedYears = new Set(); // To track inserted years
let selectedRow = null; // To track the currently selected row

function setSelectedRow(row) {
    selectedRow = row;
}

async function getRows() {
    const response = await fetch('/rows/', {
        method: 'GET',
    });
    if (!response.ok) throw new Error("Network response was not ok");

    // Prepare for incoming data
    const rows = await response.json();
    console.log(rows);
    rows.forEach((row) => {
        inserTableRow(row, rows);
    });
}

// Headers is a list of strings
function setTableHeader() {
    const table = document.getElementById('lieferungen');
    const thead = table.createTHead();
    const row = thead.insertRow();
    columns.forEach((header) => {
        const th = document.createElement('th');
        if (header === "checkbox") {
            th.textContent = "";
        }
        else {
            th.textContent = header;
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
    const table = document.getElementById('lieferungen-body');
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
            checkbox.addEventListener('change', (event) => {
                setSelectedRow(event.target.checked ? rowData : null);
            });
            cell.appendChild(checkbox);
        }
        else if (column === "bestätigungs-button") {
            const button = document.createElement('button');
            button.textContent = '✔';
            button.addEventListener('click', () => {
                // Handle button click event here
                console.log(`Bestätigen button clicked for row: ${JSON.stringify(rowData)}`);
            });
            cell.appendChild(button);
        }
        else if (column === "neue_kw-nummerfeld") {
            const input = document.createElement('input');
            input.type = 'number';
            input.style.width = '90%';
            input.value = rowData["neue_kw"] || '';
            cell.appendChild(input);
        }
        else if (column === "lieferverzugs-grund-textfeld") {
            const input = document.createElement('input');
            input.type = 'text';
            input.style.width = '90%';
            input.value = rowData["lieferverzugs_grund"] || '';
            cell.appendChild(input);
        }
        else if (column === "jahr") {
            if (!insertedYears.has(rowData["jahr"])) {
                cell = row.insertCell();
                cell.className = column; // Assign class name for styling
                cell.textContent = rowData[column] || '';
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
                else {
                    cell.style.backgroundColor = 'green';
                }
            }
        }
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