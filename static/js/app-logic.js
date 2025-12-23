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