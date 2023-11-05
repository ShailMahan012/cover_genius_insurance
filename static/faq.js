const faqs = document.querySelectorAll(".custom_class_faq")

function open_faq(div) {
    let parent = div.parentNode
    let sibling = div.nextElementSibling

    parent.classList.toggle("active")
    if (parent.classList.contains("active")) {
        sibling.style.maxHeight = ""
    }
    else {
        sibling.style.maxHeight = "0"
    }
}

for(let i=0;i<faqs.length;i++) {
    let faq = faqs[i]
    faq.onclick = ()=> {
        open_faq(faqs[i])
    }
}
