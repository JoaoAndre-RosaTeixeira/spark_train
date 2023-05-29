togglePopup()

let tables = [];
let datas = null
fetch('/get_tables', {
    method: 'GET'
})
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then(json => {

        tables = json.tables
        // Process the response data
    })
    .catch(error => {
        console.error(error);
    })
    .finally(() => {
        call_events();
    });

document.getElementById('data-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);


    fetch('/select_data', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                datas = response.json()
                togglePopup()
                return datas
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(json => {
            console.log(json);

            // Process the response data
        })
        .catch(error => {
            console.error(error);
        })
        .finally(() => {
            console.log(formData); // Vérifiez les valeurs ajoutées à FormData avant l'envoi
            display_datas()

        });
});

let tables_choice = []

function choiceTable(table) {
    console.log(table.value);
    table = table.value


    if (tables_choice.includes(table)) {
        var index = tables_choice.indexOf(table);
        tables_choice.splice(index, 1);
    } else {
        tables_choice.push(table);
    }

    console.log(tables_choice);
}

function call_events() {
    for (let tbl of tables) {
        let checkbox = document.querySelector('#' + tbl);
        checkbox.addEventListener('change', function (event) {
            show_div = document.querySelector('#' + tbl + "_show");
            if (show_div.style.display === 'none') {
                show_div.style.display = 'grid';
            } else {
                show_div.style.display = 'none';
            }
        });
    }
}


function display_datas() {
    let container = document.querySelector(".container_datas");
    container.innerHTML = ""; // Efface le contenu existant
    console.log(datas);
    datas.then(function (resolvedData) {
        let table = document.createElement("table");
        let tableHeader = document.createElement("tr");

        // Crée l'en-tête du tableau avec les clés de l'objet
        for (let key in resolvedData[0]) {
            let th = document.createElement("th");
            th.textContent = key;
            tableHeader.appendChild(th);
        }
        table.appendChild(tableHeader);

        // Parcours les données et crée les lignes du tableau
        for (let data of resolvedData) {
            let tableRow = document.createElement("tr");

            for (let val in data) {
                let td = document.createElement("td");
                td.textContent = data[val];
                tableRow.appendChild(td);
            }

            table.appendChild(tableRow);
        }

        container.appendChild(table);
    });
}

