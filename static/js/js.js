const menu = document.querySelector(".menu")
const bar = document.querySelector(".bar")



menu.addEventListener('click',()=>{
        bar.classList.toggle('mobile')
})

document.body.addEventListener("htmx:responseError",function(evt){
            alert(evt.detail.xhr.responseText)
})

function getCategoriePk(cat_pk){
    let add_m = document.getElementById("add_m");
    let supp_c = document.getElementById("del_cat");
    add_m.setAttribute("value",cat_pk);
    supp_c.setAttribute("value",cat_pk);
}

function getFonctionPk(fonc_pk){
    let add_e = document.getElementById("add_e");
    let supp_f = document.getElementById("del_fonc");
    add_e.setAttribute("value",fonc_pk);
    supp_f.setAttribute("value",fonc_pk);
}


function myFunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}



