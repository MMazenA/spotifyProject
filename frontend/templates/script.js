var image_div = document.getElementById("image_div");
var song_name_div = document.getElementById("song_name_div");

var eventSource = new EventSource("/stream");
eventSource.onmessage = function (e) {
    image_div.innerHTML = "<img src='" + JSON.parse(e.data).pic_link + "'/>";
    song_name_div.innerHTML = JSON.parse(e.data).song_name
};