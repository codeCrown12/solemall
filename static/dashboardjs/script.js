var btnbars = document.querySelector(".btn-bars");

btnbars.addEventListener('click', ()=>{
    if (document.getElementById("sidebar").style.width === "60%") {
        document.getElementById("sidebar").style.width = "0"
        btnbars.innerHTML = "<i class='fas fa-bars'></i>"
    }
    else{
        document.getElementById("sidebar").style.width = "60%"
        btnbars.innerHTML = "<i class='fas fa-times'></i>";
    }
})