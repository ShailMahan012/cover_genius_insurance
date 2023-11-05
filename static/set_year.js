const footer_year = document.getElementById("custom_year")

function set_year() {
    const d = new Date();
    let year = d.getFullYear();
    footer_year.innerHTML = year;
}

set_year()