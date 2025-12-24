/**
 * App Logic - PerSec Rendszer
 * Egységesített eseménykezelés a kereséshez és adatbevitelhez
 */

window.addEventListener('load', function () {
    console.log("App Logic 1.4 betöltve...");

    // 1. BOOTSTRAP INICIALIZÁLÁS (Tooltip, Dropdown)
    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(t => new bootstrap.Tooltip(t));

        const dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dd => new bootstrap.Dropdown(dd));
    } else {
        console.error("HIBA: A Bootstrap motor nem töltődött be!");
    }

    // 2. MODAL FOCUS ÉS ENTER FIGYELÉS
    const searchModal = document.getElementById('mdl_Search');
    if (searchModal) {
        searchModal.addEventListener('shown.bs.modal', function () {
            const input = document.getElementById('requesterData');
            if (input) input.focus();
        });
    }

    const requesterData = document.getElementById('requesterData');
    if (requesterData) {
        requesterData.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                executeSearch(); // Ez hívja meg a lenti globális függvényt
            }
        });
    }

    // 3. ÚJ SZEMÉLY MODAL (mdl_AddNewPerson) LOGIKA
    const addNewPersonModal = document.getElementById('mdl_AddNewPerson');
    if (addNewPersonModal) {
        addNewPersonModal.addEventListener('show.bs.modal', function () {
            const form = addNewPersonModal.querySelector('form');
            if (form) form.reset();

            const inputs = addNewPersonModal.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.name !== 'valid_e') {
                    input.value = "";
                    if (input.tagName === 'SELECT') {
                        input.selectedIndex = 0;
                    }
                }
            });

            const szulNevInput = document.getElementById('input_szuletesiNev');
            if (szulNevInput) szulNevInput.style.backgroundColor = "";
        });
    }
});

// --- GLOBÁLIS FÜGGVÉNYEK (Ezeket látja a HTML onclick) ---

/**
 * Keresés indítása - Meghívva: onclick="executeSearch()"
 */
function executeSearch() {
    console.log("!!! MANUÁLIS FÜGGVÉNY INDÍTVA !!!");

    const requesterData = document.getElementById('requesterData');
    if (!requesterData) return;

    const searchName = requesterData.value.trim();

    if (searchName === "") {
        requesterData.focus();
        return;
    }

    let status = "all";
    if (document.getElementById('btnradio_Aktiv').checked) status = "active";
    else if (document.getElementById('btnradio_Inaktiv').checked) status = "inactive";

    const langSwitch = document.getElementById('langSensitivity');
    const isStrict = langSwitch ? langSwitch.checked : true;

    const targetUrl = "/resultNameSearch?query=" + encodeURIComponent(searchName) +
                      "&status=" + status +
                      "&strict=" + isStrict;

    console.log("Keresés indítása: ", targetUrl);
    window.open(targetUrl, '_blank');

    // Modal bezárása
    const modalEl = document.getElementById('mdl_Search');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) modalInstance.hide();
}
/*Flash eleje*/
function closeFeedback() {
    const modal = document.getElementById("systemFeedbackModal");
    if (modal) {
        modal.classList.remove("show");
        // Megvárjuk az animációt, mielőtt eltüntetjük
        setTimeout(() => {
            modal.style.display = "none";
        }, 300);
    }
}

// Ha a háttérre kattint, akkor is záródjon be
window.addEventListener("click", function(event) {
    const modal = document.getElementById("systemFeedbackModal");
    if (event.target === modal) {
        closeFeedback();
    }
});
/*Flash vége*/
/**
 * Név másolása Jelenlegi név -> Születési név
 * Meghívva: onclick="copyName()"
 */
function copyName() {
    const inputNev = document.getElementById('input_nev');
    const inputSzulNev = document.getElementById('input_szuletesiNev');

    if (inputNev && inputSzulNev) {
        const nevVal = inputNev.value.trim();
        if (nevVal !== "") {
            inputSzulNev.value = nevVal;
            inputSzulNev.style.backgroundColor = "rgba(226, 178, 117, 0.2)";
            setTimeout(() => {
                inputSzulNev.style.backgroundColor = "";
            }, 300);
        }
    }
}

/**
 * Személyi adatlap megnyitása és feltöltése
 */
function loadAndOpenDetails(personId) {
    console.log("Kattintás észlelve, ID:", personId);
    const modalEl = document.getElementById('mdl_PersonDetails');
    if (!modalEl) {
        console.error("HIBA: A 'mdl_PersonDetails' nevű modal nem található a HTML-ben!");
        alert("Hiba: A modal struktúra hiányzik az oldalról!");
        return;
    }
    fetch(`/get_person_details/${personId}`)
        .then(response => {
            if (!response.ok) throw new Error('Hálózati hiba, vagy hiányzó rekordId');
            return response.json();
        })
        .then(data => {
            console.log("Szerver válasza:", data);
            document.getElementById('detail_header_full_name').innerText = (data.titulus ? data.titulus + " " : "") + data.nev;
            const statusContainer = document.getElementById('detail_header_status');
            if (statusContainer) {
                if (data.valid_e == 1 || data.valid_e === true) {
                    statusContainer.innerHTML = '<span class="badge rounded-pill" style="background-color: #198754 !important; color: #ffffff !important; border: 1px solid #ffffff !important; box-shadow: 0 0 10px rgba(25, 135, 84, 0.8) !important; text-transform: uppercase;">Aktív</span>';
                } else {
                    statusContainer.innerHTML = '<span class="badge rounded-pill" style="background-color: #dc3545 !important; color: #ffffff !important; border: 1px solid #ffffff !important; box-shadow: 0 0 10px rgba(220, 53, 69, 0.8) !important; text-transform: uppercase;">Archivált</span>';
                }
            }
            document.getElementById('detail_header_full_name').innerText = (data.titulus ? data.titulus + " " : "") + data.nev;
            document.getElementById('det_titulus').value = data.titulus || '';
            document.getElementById('det_nev').value = data.nev || '';
            document.getElementById('det_szuletesiNev').value = data.szuletesiNev || '';
            document.getElementById('det_szuletesiHely').value = data.szuletesiHely || '';
            document.getElementById('det_szuletesiIdo').value = data.szuletesiIdo || '';
            document.getElementById('det_anyjaNeve').value = data.anyjaNeve || '';
            document.getElementById('det_rendfokozat').value = data.rendfokozat;
            document.getElementById('det_beosztas').value = data.beosztas;
            document.getElementById('det_szervezetiElem').value = data.szervezetiElem;
            document.getElementById('det_memo').value = data.memo;
            const teljesNev = (data.titulus ? data.titulus + " " : "") + data.nev;
            document.getElementById('dash_nev').innerText = teljesNev;
            const rfSelect = document.getElementById('det_rendfokozat');
            const rfText = rfSelect.options[rfSelect.selectedIndex] ? rfSelect.options[rfSelect.selectedIndex].text : "-";
            document.getElementById('dash_rendfokozat').innerText = rfText;
            const beoSelect = document.getElementById('det_beosztas');
            const beoText = beoSelect.options[beoSelect.selectedIndex] ? beoSelect.options[beoSelect.selectedIndex].text : "-";
            document.getElementById('dash_beosztas').innerText = beoText;

            // Bal oldali szerkeszthető mezők (ID-val állítjuk be a select-et)
document.getElementById('det_rendfokozat').value = data.rendfokozat_id;
document.getElementById('det_beosztas').value = data.beosztas_id;

// Jobb oldali Dashboard (A szöveges nevet írjuk ki)
document.getElementById('dash_rendfokozat').innerText = data.rendfokozat_nev;
document.getElementById('dash_beosztas').innerText = data.beosztas_nev;

// Dashboard adatok frissítése (Jobb oldal)
const nemzetiContainer = document.getElementById('dash_nemzeti');

if (data.nemzeti_szint) {
    // Összeállítjuk a neonos badge-et (stílus a szemelyibiztonsag.html alapján)
    nemzetiContainer.innerHTML = `
        <div class="d-flex flex-column align-items-center gap-3">
            <span class="badge border"
                  style="min-width: 120px; border-color: #ffb300 !important; color: #ffb300 !important;
                         background: rgba(255, 179, 0, 0.1); font-weight: bold; text-transform: uppercase;
                         font-size: 0.8rem; box-shadow: 0 0 15px rgba(255, 179, 0, 0.4); padding: 8px 12px;">
                ${data.nemzeti_szint}
            </span>
            <div class="text-white-50 small">
                <i class="bi bi-calendar3 me-1"></i> Érvényes:
                <span class="text-white fw-bold">${data.nemzeti_ervenyesseg}</span>
            </div>
        </div>
    `;
} else {
    nemzetiContainer.innerHTML = '<div class="text-muted italic small py-3">Nincs minősítés</div>';
}





            // Kényszerített indítás
            const detailsModal = new bootstrap.Modal(modalEl);
            detailsModal.show();
        })
        .catch(err => {
            console.error("AJAX hiba:", err);
            alert("Nem sikerült betölteni az adatokat! (ID: " + personId + ")");
        });
}

function sortAgentTable(column, direction) {
    const table = document.querySelector(".table-viewport table");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    // Rendezési logika
    const sortedRows = rows.sort((a, b) => {
        let valA, valB;

        if (column === 'nev') {
            // Név lekérése a második oszlopból (index 1)
            valA = a.cells[1].innerText.trim().toLowerCase();
            valB = b.cells[1].innerText.trim().toLowerCase();

            // Magyar ékezetes karakterek helyes kezelése (localeCompare)
            return direction === 'asc'
                ? valA.localeCompare(valB, 'hu')
                : valB.localeCompare(valA, 'hu');
        }

        else if (column === 'date') {
            // Dátum lekérése az utolsó oszlopból (index 7)
            // A "---" vagy üres értékeket a végére tesszük
            valA = a.cells[7].innerText.trim();
            valB = b.cells[7].innerText.trim();

            if (valA === "---") valA = "0000.00.00.";
            if (valB === "---") valB = "0000.00.00.";

            return direction === 'asc'
                ? valA.localeCompare(valB)
                : valB.localeCompare(valA);
        }
    });

    // A régi sorok eltávolítása és az újak hozzáadása
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    sortedRows.forEach(row => tbody.appendChild(row));

    // Opcionális: Vizuális visszajelzés (ikonok színezése)
    updateSortIcons(column, direction);
}

function updateSortIcons(column, direction) {
    // Összes ikon alaphelyzetbe
    document.querySelectorAll('.sort-icon').forEach(icon => icon.classList.remove('active'));

    // Az aktuálisan kiválasztott ikon kiemelése
    // Ez feltételezi, hogy az onclick eseményben átadod melyik oszlop/irány
    // (A HTML-ben a korábban javasolt módon kell lennie)
}