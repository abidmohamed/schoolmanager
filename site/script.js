document.getElementById("language-select").addEventListener("change", function() {
    var selectedLanguage = this.value;
    if (selectedLanguage === "ar") {
        document.documentElement.setAttribute("dir", "rtl");
    } else {
        document.documentElement.removeAttribute("dir");
    }
});

document.getElementById("theme-toggle").addEventListener("change", function() {
    if (this.checked) {
        document.body.classList.add("dark-theme");
    } else {
        document.body.classList.remove("dark-theme");
    }
});