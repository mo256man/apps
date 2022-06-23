function timer(){
    var now = dayjs();

    // 1分に1回実行
    if ((now.minute() != lastminute) && isDone) {
        isDone = false;
        lastminute = now.minute();
        console.log("try start");
        $.ajax({
            type : "POST",
            url  : "/getCamera"
        }).done(function(data) {
            console.log("done");
            isDone = true;
            data = JSON.parse(data);
            putImage(data);
        }).fail(function(jqXHR, textStatus, errorThrown){
            console.log("fail");
            console.log(jqXHR, textStatus, errorThrown);            
        });
    }

    // 1時間に1回実行
    if ((now.hour() != lasthour) && isDone) {
        isDone = false;
        lasthour = now.hour();
        $.ajax({
            type : "POST",
            url  : "/getCurrentTenki"
        })
        .done(function(data) {
            isDone = true;
            data = JSON.parse(data);
            writeData(data);
        });
    }
};


function changeDate(k) {
    date = date.add(k, "day");
    strDate = date.format("YYYY/MM/DD");
    $("#date").text(strDate);
    $.ajax({
        type : "POST",
        url  : "/getDailyTenki",
        data: {"date": strDate}
    })
    .done(function(data) {
        daily_weather = JSON.parse(data);
        writeData(daily_weather);
    });
}

function writeData(daily_weather){
    for (var h=0; h<24; h++) {
        $("#i"+h).html("");
        $("#r"+h).text("");
        $("#t"+h).text("");
        $("#h"+h).text("");
        $("#w"+h).text("");
    };
    var data_cnt = Object.keys(daily_weather).length;
    if (data_cnt > 0) {
        for (var i=0; i<data_cnt; i++) {
            var h = daily_weather[i]["hour"];
            $("#i"+h).html("<img src='../static/icons/" + daily_weather[i]["icon"] + ".png'>");
            $("#r"+h).text(daily_weather[i]["rain"]);
            $("#t"+h).text(daily_weather[i]["temp"]);            
            $("#h"+h).text(daily_weather[i]["humidity"]);
            $("#w"+h).text(daily_weather[i]["wind_speed"]);
        };
    };
};


function putImage(data) {
    $("#image1").attr("src", "data:image/jpg;base64," + data["image1"]);
    $("#image2").attr("src", "data:image/jpg;base64," + data["image1"]);
}



var isDone = true;
var k = 0;
var lasthour = dayjs().hour();
var lastminute = dayjs().minute();
var data = [];
var date = dayjs();
var strDate = date.format("YYYY/MM/DD");
changeDate(k);
setInterval(() => {
    timer();
}, 1000);