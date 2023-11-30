aqi_text = document.getElementById("aqi-info")

let red = aqi_text.getAttribute('data-aqi-red')
let green = aqi_text.getAttribute('data-aqi-green')
let blue = aqi_text.getAttribute('data-aqi-blue')

aqi_text.style.color = `rgb(${red},${green},${blue})`