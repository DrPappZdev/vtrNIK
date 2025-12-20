// Megvárjuk, amíg az ablak és minden erőforrás betölt

window.addEventListener('load', function () {
    console.log("App Logic betöltve...");

    if (typeof bootstrap !== 'undefined') {
        // 1. Tooltip-ek inicializálása (az Offcanvas-ban lévők is!)
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(t => new bootstrap.Tooltip(t));

        // 2. Kereső Modal fókuszálás (ezt már ismered)
        const searchModal = document.getElementById('mdl_Search');
        if (searchModal) {
            searchModal.addEventListener('shown.bs.modal', function () {
                const input = document.getElementById('requesterData');
                if (input) input.focus();
            });
        }

        // 3. Dropdown-ok kényszerített inicializálása (opcionális, ha nem nyílnának)
        const dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dd => new bootstrap.Dropdown(dd));

    } else {
        console.error("HIBA: A Bootstrap motor nem töltődött be!");
    }
});








    // 3. Keresés gomb (ez bootstrap nélkül is mehet)
    const searchBtn = document.getElementById("searchBtn");
    if (searchBtn) {
        searchBtn.addEventListener("click", function () {
            const query = document.getElementById("requesterData").value;
            if (query.trim() === "") {
                alert("Kérlek előbb írj be valamit!");
            } else {
                console.log("Keresés indítása: " + query);
            }
        });
    }
});