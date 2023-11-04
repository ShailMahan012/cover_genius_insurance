const nav_open_img = document.getElementById("nav_open_img")
const nav_close_img = document.getElementById("nav_close_img")
const nav_menu = document.getElementById("nav_menu")

function nav_open() {
    nav_open_img.style.display = "none"
    nav_close_img.style.display = "block"

    nav_menu.style.transform = "translateX(0)"
}

function nav_close() {
    nav_open_img.style.display = "block"
    nav_close_img.style.display = "none"

    nav_menu.style.transform = "translateX(-100vw)"
}
