function timer(){
    var now = dayjs();
    if (now.hour() != lasthour) {
        lasthour = now.hour();
        $.ajax({
            type : "GET",
            url  : "/ajax"
        })
        .done(function() {
            alert(data);
        });
    }
};



var lasthour = -1;
alert(lasthour);
setInterval(() => {
    timer();
}, 1000);
