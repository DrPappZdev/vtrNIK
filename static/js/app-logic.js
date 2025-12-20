window.addEventListener('load', function () {
    console.log("App Logic betöltve...");

    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(t => new bootstrap.Tooltip(t));

        const searchModal = document.getElementById('mdl_Search');
        if (searchModal) {
            searchModal.addEventListener('shown.bs.modal', function () {
                const input = document.getElementById('requesterData');
                if (input) input.focus();
            });
        }

        const dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dd => new bootstrap.Dropdown(dd));

    } else {
        console.error("HIBA: A Bootstrap motor nem töltődött be!");
    }
});

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
    };