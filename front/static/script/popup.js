console.log("HELLO POPUP")
let popup = document.querySelector("#popup");
console.log(popup)

function togglePopup() {

    if (popup.style.display === "none") {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
}
//
// function get_datas(){
//     return datas
// }