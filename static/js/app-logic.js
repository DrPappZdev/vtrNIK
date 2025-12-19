// Megvárjuk, amíg az ablak és minden erőforrás betölt
window.addEventListener('load', function () {
    console.log("App Logic betöltve...");

    // Ellenőrizzük, hogy a bootstrap objektum létezik-e
    if (typeof bootstrap !== 'undefined') {
        console.log("Bootstrap motor aktív.");

        // 1. Tooltip-ek (csak ha vannak)
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(t => {
            try {
                new bootstrap.Tooltip(t);
            } catch (e) {
                console.warn("Tooltip hiba egy elemnél:", e);
            }
        });

        // 2. Modal fókuszálás
        const searchModal = document.getElementById('mdl_Search');
        if (searchModal) {
            searchModal.addEventListener('shown.bs.modal', function () {
                const input = document.getElementById('requesterData');
                if (input) input.focus();
            });
        }
    } else {
        console.error("HIBA: A Bootstrap motor nem töltődött be!");
    }

    // 3. Keresés gomb (ez bootstrap nélkül is mehet)
    const searchBtn = document.getElementById("searchBtn");
    if (searchBtn) {
        searchBtn.addEventListener("click", function () {
            const query = document.getElementById("requesterData").value;
            if (query.trim() === "") {
                alert("Kérlek írj be valamit!");
            } else {
                console.log("Keresés indítása: " + query);
            }
        });
    }
});