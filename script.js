document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed")
    var button = document.getElementById("toggleButton");
    var table = document.getElementById("weather-table");
    let element = document.getElementById('toggleButton');

    table.style.display = "none";

    button.addEventListener("click", function() {
        console.log("Button clicked");
        if (table.style.display === "none") {
            table.style.display = "block";
            element.innerHTML = "Hide forecast Data";
        } else {
            table.style.display = "none";
            element.innerHTML = "Show forecast Data";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let body = document.querySelector('body');
    let original_color = getComputedStyle(body).color;
    let original_background = getComputedStyle(body).backgroundColor;

    body.style.backgroundColor = original_background;

    document.querySelector('#light').addEventListener('click', function() {
        console.log("button");
        let element = document.getElementById('light');
        if (body.style.backgroundColor == original_background)
        {
            body.style.backgroundColor = 'black';
            body.style.color = 'white';
            element.innerHTML = "Dark Mode";
        }
        else
        {
            body.style.backgroundColor = original_background;
            body.style.color = original_color;
            element.innerHTML = "Light Mode";
        }


    });
});


