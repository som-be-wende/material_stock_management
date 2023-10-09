const menu = document.querySelector("#menu");
const bar = document.querySelector(".bar");



menu.addEventListener('click',()=>{
        bar.classList.toggle('mobile')
});



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

function stock_value() {
  var v_stock = document.getElementById("v_stock"); //on récupère les lignes du tableau
  var arrayLignes = document.getElementById("tab_mat").rows; //on récupère les lignes du tableau
  var longueur = arrayLignes.length; //on peut donc appliquer la propriété length

  t = 0;
  for (var i = 1; i < longueur; i++) {
    var arrayColonnes = arrayLignes[i].cells; //on récupère les cellules de la ligne
    var largeur = arrayColonnes.length;
    arrayColonnes[6].innerHTML =
      arrayColonnes[5].innerHTML * arrayColonnes[4].innerHTML;
    t += arrayColonnes[5].innerHTML * arrayColonnes[4].innerHTML;
  }

  v_stock.innerHTML = t;
}

