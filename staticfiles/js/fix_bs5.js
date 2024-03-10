
// Get all ckeditor fields
let ckeditors = document.getElementsByClassName("django-ckeditor-widget")
let images = document.getElementsByClassName("clearablefileinput")


// Update ckeditor CSS to adapte it with Bootstrap5
for (const key of Object.keys(ckeditors)) {
    ckeditors[key].classList.add("form-control");
}


// Update images CSS to adapte it with Bootstrap5
for (const key of Object.keys(images)) {
    images[key].classList.add("form-control");
}


