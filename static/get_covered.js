const covers = document.getElementById("covers_ul")
const works = document.getElementById("works_ul")
const claim = document.getElementById("claim_ul")

const covers_div = document.getElementById("covers_div")
const works_div = document.getElementById("works_div")
const claim_div = document.getElementById("claim_div")


const covers_indicator = document.getElementById("covers_indicator")
const works_indicator = document.getElementById("works_indicator")
const claim_indicator = document.getElementById("claim_indicator")

const vehicle_type = document.getElementById("type")
const dob = document.getElementById("dob")

const show_cover_btn_class = "col text-nowrap flex-nowrap text-center cursor-pointer text-capitalize py-1 text-green fw-500"
const hide_cover_btn_class = "col text-nowrap flex-nowrap text-center cursor-pointer text-capitalize py-1 text-gray-500 fw-300"


function show_covers() {
    covers.style.display = "block"
    works.style.display = "none"
    claim.style.display = "none"

    covers_div.className = show_cover_btn_class
    works_div.className = hide_cover_btn_class
    claim_div.className = hide_cover_btn_class

    covers_indicator.style.display = "block"
    works_indicator.style.display = "none"
    claim_indicator.style.display = "none"
}

function show_works() {
    covers.style.display = "none"
    works.style.display = "block"
    claim.style.display = "none"

    covers_div.className = hide_cover_btn_class
    works_div.className = show_cover_btn_class
    claim_div.className = hide_cover_btn_class

    covers_indicator.style.display = "none"
    works_indicator.style.display = "block"
    claim_indicator.style.display = "none"
}

function show_claim() {
    covers.style.display = "none"
    works.style.display = "none"
    claim.style.display = "block"

    covers_div.className = hide_cover_btn_class
    works_div.className = hide_cover_btn_class
    claim_div.className = show_cover_btn_class

    covers_indicator.style.display = "none"
    works_indicator.style.display = "none"
    claim_indicator.style.display = "block"
}



const sidebar_1 = document.getElementById("sidebar_1")
const sidebar_2 = document.getElementById("sidebar_2")
const sidebar_3 = document.getElementById("sidebar_3")

function get_covered() {
    sidebar_1.style.display = "none"
    sidebar_2.style.display = "block"
}

function show_summary() {
    if (vehicle_type.value && dob.validity.valid) {
        let data = JSON.stringify({
            dob: dob.value,
            vehicle_type: vehicle_type.value,
        })
        fetch("/save_vehicle", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: data
        })
        .then(resp=> {
            return resp.text()
        })
        .then(resp=> {
            if (resp == "true") {
                sidebar_2.style.display = "none"
                sidebar_3.style.display = "block"
            }
            else {
                window.location.href = "/signup"
            }
        })
    }
    else {
        vehicle_type.reportValidity()
        dob.reportValidity()
    }
}

covers_div.onclick = show_covers
works_div.onclick = show_works
claim_div.onclick = show_claim
