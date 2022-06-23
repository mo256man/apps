function call_python(k){
    data = {"button": k};
    send_json = JSON.stringify(data);           // JSON文字列に変換

    $.ajax({
        type: "POST",
        url: "/ajax",                           // Flaskのルーティング
        data: send_json,                        // 送るJSONデータ
        contentType: 'application/json; charset=UTF-8',
        headers: {'Content-Type': 'application/json'},
        })
        
        // ここからがPythonからの戻り値を使う処理
        .done(function(received_json) {
            $("#date").text(received_json["date"]);
            $('#img1').attr("src", "data:image/jpeg;base64," + received_json["img1"]);
            $('#img2').attr("src", "data:image/jpeg;base64," + received_json["img2"]);
            if (received_json["status"] != "") {
                $("#status").text(received_json["status"] + "が押された状態にある");
            } else {
                $("#status").text("");
            };
        }).fail (function(XMLHttpRequest, textStatus, errorThrown){
            console.log(XMLHttpRequest.status);
            console.log(textStatus);
            console.log(errorThrown);
        });
}



function push_button(k) {
// ボタンが押されたときの処理
    call_python(k);
}


setInterval(function(){call_python()}, 1000);