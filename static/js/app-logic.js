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
        console.error("HIBA: A 'mdl_PersonDetails' nevű modal nem található!");
        return;
    }

    fetch(`/get_person_details/${personId}`)
        .then(response => {
            if (!response.ok) throw new Error('Hálózati hiba');
            return response.json();
        })
        .then(data => {
            console.log("Szerver válasza:", data);

            // --- 1. ALAPADATOK BETÖLTÉSE ---
            const teljesNev = (data.titulus ? data.titulus + " " : "") + data.nev;
            document.getElementById('detail_header_full_name').innerText = teljesNev;
            document.getElementById('dash_nev').innerText = teljesNev;

            // Státusz badge (Aktív/Archivált)
            const statusContainer = document.getElementById('detail_header_status');
            if (statusContainer) {
                if (data.valid_e == 1 || data.valid_e === true) {
                    statusContainer.innerHTML = '<span class="badge rounded-pill bg-success border border-white shadow-sm">AKTÍV</span>';
                } else {
                    statusContainer.innerHTML = '<span class="badge rounded-pill bg-danger border border-white shadow-sm">ARCHIVÁLT</span>';
                }
            }

            // Input mezők kitöltése
            document.getElementById('det_titulus').value = data.titulus || '';
            document.getElementById('det_nev').value = data.nev || '';
            document.getElementById('det_szuletesiNev').value = data.szuletesiNev || '';
            document.getElementById('det_szuletesiHely').value = data.szuletesiHely || '';
            document.getElementById('det_szuletesiIdo').value = data.szuletesiIdo || '';
            document.getElementById('det_anyjaNeve').value = data.anyjaNeve || '';
            document.getElementById('det_rendfokozat').value = data.rendfokozat_id;
            document.getElementById('det_beosztas').value = data.beosztas_id;
            document.getElementById('det_szervezetiElem').value = data.szervezetiElem || '';
            document.getElementById('det_memo').value = data.memo || '';

            // Dashboard szövegek
            document.getElementById('dash_rendfokozat').innerText = data.rendfokozat_nev || '-';
            document.getElementById('dash_beosztas').innerText = data.beosztas_nev || '-';

            // --- 2. NEMZETI BIZTONSÁGI KÁRTYA LOGIKA ---
            const nemzetiContainer = document.getElementById('dash_nemzeti');

            if (data.nemzeti_szint && data.nemzeti_ervenyesseg !== "---") {
                // MAI DÁTUM (időpont nélkül az összehasonlításhoz)
                const ma = new Date();
                ma.setHours(0, 0, 0, 0);

                // LEJÁRATI DÁTUM KONVERTÁLÁSA (YYYY.MM.DD. -> YYYY-MM-DD)
                // A JS a kötőjeles formátumot szereti, az utolsó pontot pedig levágjuk
                const lejaratTiszta = data.nemzeti_ervenyesseg.replaceAll('.', '-').replace(/-$/, '');
                const lejaratDate = new Date(lejaratTiszta);

                // Különbség napokban
                const diffTime = lejaratDate - ma;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

                // Neon badge kiválasztása
                let countdownHtml = '';
                if (diffDays > 0) {
                    countdownHtml = `<div class="badge-neon-green mt-2">Még ${diffDays} nap</div>`;
                } else if (diffDays === 0) {
                    countdownHtml = `<div class="badge-neon-red mt-2">MA JÁR LE!</div>`;
                } else {
                    countdownHtml = `<div class="badge-neon-red mt-2">LEJÁRT (${Math.abs(diffDays)} napja)</div>`;
                }

                // Kártya felépítése
                // Kártya összeállítása kattintható konténerrel
                nemzetiContainer.style.cursor = "pointer"; // Hogy látszódjon: kattintható
                nemzetiContainer.setAttribute("onclick", "openNemzetiDetails()"); // Kattintásra hívja a függvényt

                nemzetiContainer.innerHTML = `
                    <div class="d-flex flex-column align-items-center hover-card-effect">
                        <div class="text-uppercase fw-bold mb-1" style="color: #e2b275; font-size: 0.7rem; letter-spacing: 2px;">NEMZETI</div>
                        <div class="text-white fw-bold mb-1" style="font-size: 1.1rem;">${data.nemzeti_szint}</div>
                        <div class="text-white-50 small mb-1">${data.nemzeti_ervenyesseg}</div>
                        ${countdownHtml}
                    </div>
                `;
            } else {
                nemzetiContainer.innerHTML = '<div class="text-muted italic small py-3">Nincs adat</div>';
            }

            // --- 3. MODAL MEGJELENÍTÉSE ---
            const detailsModal = new bootstrap.Modal(modalEl);
            detailsModal.show();
        })
        .catch(err => {
            console.error("Hiba az adatok betöltésekor:", err);
            alert("Hiba történt az adatlap megnyitásakor!");
        });
}

function openNemzetiDetails() {
    // Inicializáljuk és megnyitjuk a második modalt
    const nemzetiModal = new bootstrap.Modal(document.getElementById('mdl_NemzetiDetails'));
    nemzetiModal.show();
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