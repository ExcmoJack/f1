import obj_fileJson from "../../data/files.json" with { type: "json" };
// obj_fileJson = null;

obj_calendarJson = null;
obj_pointsJson = null;
obj_driversJson = null;
obj_constructorsJson = null;
obj_teamFullNamesJson = null;

init();
main();


function init() {
    obj_fileJson = getDataFromJson("files");
    console.log(obj_fileJson);
};

function main() {
    setInterval(updateCountdown, 500);
};

function getDataFromJson(str_filename) {
    let parent = window.location.pathname;
    var jsonContent;
    const requestURL = parent + "data/" + str_filename + ".json";
    const request = new XMLHttpRequest();

    request.open("GET", requestURL);

    request.responseType = "json";
    request.send();

    request.onload = function () {
        jsonContent = request.response;
    };

    return jsonContent;
};

function updateCountdown() {
    let date_currentDate = new Date();
    let str_nextEventTitle = 'Grand Prix of Australia';
    let int_nextEventTime = 600;
    let arr_nextEventDate = [16, 2, 2025];
    let date_nextEventDate = new Date(arr_nextEventDate[2], arr_nextEventDate[1], arr_nextEventDate[0], int_nextEventTime / 100, int_nextEventTime % 100);
    let int_differenceMs = date_nextEventDate.getTime() - date_currentDate.getTime();
    let int_countdownSeconds = Math.floor(int_differenceMs / 1000) % 60;
    let int_countdownMinutes = ((Math.floor(int_differenceMs / 1000) - int_countdownSeconds) / 60) % 60;
    let int_countdownHours = Math.floor((((Math.round(int_differenceMs / 1000) - int_countdownSeconds) / 60) - int_countdownMinutes) / 60) % 24;
    let int_countdownDays = (Math.floor((((Math.round(int_differenceMs / 1000) - int_countdownSeconds) / 60) - int_countdownMinutes) / 60) - int_countdownHours) / 24;

    document.getElementById("countdown_event").innerText = str_nextEventTitle + " " + arr_nextEventDate[2];
    document.getElementById("countdown_remaining").innerText = int_countdownDays + " days, " + int_countdownHours + " hours, " + int_countdownMinutes + " minutes, " + int_countdownSeconds + " seconds";
};