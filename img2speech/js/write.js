let startX = 0;
let startY = 0;
let write = 0;
let mousedown = false;
let img_datas_cnt = 0;
let text = "";
let img_datas_arr = [];

function addtext() {
    text += t[maxScoreIndex].toLowerCase()
    remove_text()
    if (conf[3] === "on"){
        show_msg("ok","文字を追加しました:"+t[maxScoreIndex].toLowerCase()+"<br>現在の文字:"+text)
    }
}

function remove_one_text() {
    if (write === 1) {
        remove_text()
    } else {
        write = 0
        text = text.slice(0, -1);
        try {
            clearInterval(PassageID);
        } catch (e) {
            console.warn(e);
        }
    }
    document.getElementById("result-text").innerHTML = "<h3>書かれていません</h3> " +
        "<p class='border-bottom'>横の四角に文字を書いてください。</p>" +
        "<br><p class='sentaku'>文字:<span id='text'>" + text + "</span></p>";
}

function remove_text() {
    img_datas_arr = []
    write = 0
    ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    if (conf[0] === "off") {
        ctx.fillStyle = "#fff";
    } else {
        ctx.fillStyle = "#000";
    }
    ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    try {
        clearInterval(PassageID);
    } catch (e) {
        console.warn(e);
    }
}

window.addEventListener('load', function () {
    canvas = document.getElementById('write');
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    let clientRect = canvas.getBoundingClientRect();
    let canvas_x = clientRect.left;
    let canvas_y = clientRect.top;
    const target = document.getElementById('write');
    const context = target.getContext('2d');
//背景色
    ctx = canvas.getContext('2d');
    if (conf[0] === "off") {
        ctx.fillStyle = "#fff";
    } else {
        ctx.fillStyle = "#000";
    }
    ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);

    //ウィンドウリサイズ時
    window.addEventListener('resize', function () {

        console.log("resize!")
        // canvasの位置座標を取得（描いたものを伸縮させないため、キャンバスの大きさを変える）
        clientRect = canvas.getBoundingClientRect();
        canvas_x = clientRect.left;
        canvas_y = clientRect.top;
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;

        // 一度消して、保存していた配列データを全て描く（ウィンドウを大きくした場合に戻す）
        if (conf[0] === "off") {
            ctx.fillStyle = "#fff";
        } else {
            ctx.fillStyle = "#000";
        }
        ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);
        ctx.strokeStyle = ""
        for (let i = 0; i < img_datas_arr.length; i++) ctx.putImageData(img_datas_arr[i], 0, 0);
    });

    canvas.addEventListener("touchstart", function (e) {
        write = 1;
        e = e.touches[0];
        startX = e.pageX - canvas_x;
        startY = e.pageY - canvas_y;
        mousedown = true;
        try {
            clearInterval(PassageID);
        } catch (e) {
            console.warn(e);
        }
        context.beginPath();
    });

    canvas.addEventListener("mousedown", function (e) {
        write = 1;
        startX = e.pageX - canvas_x;
        startY = e.pageY - canvas_y;
        mousedown = true;
        try {
            clearInterval(PassageID);
        } catch (e) {
            console.warn(e);
        }
        context.beginPath();
    });

    canvas.addEventListener("touchend", function () {
        mousedown = false;
        img_datas_arr[img_datas_cnt] = ctx.getImageData(0, 0, canvas.width, canvas.height);
        img_datas_cnt++;
        PassageID = setTimeout('addtext();', slidertime.value);
        context.closePath();
    });
    canvas.addEventListener("mouseup", function () {
        mousedown = false;
        img_datas_arr[img_datas_cnt] = ctx.getImageData(0, 0, canvas.width, canvas.height);
        img_datas_cnt++;
        PassageID = setTimeout('addtext();', slidertime.value);
        context.closePath();
    });

    canvas.addEventListener("touchmove", function (e) {
        e = e.touches[0];
        if (mousedown) draw(e.pageX - canvas_x, e.pageY - canvas_y);
    });

    window.addEventListener("mousemove", function (e) {
        if (mousedown) draw(e.pageX - canvas_x, e.pageY - canvas_y);
    });

// キャンバスに描く
    function draw(x, y) {
        context.lineCap = "round";
        context.lineWidth = 25;
        if (conf[0] === "off") {
            context.strokeStyle = "black";
        } else {
            context.strokeStyle = "white";
        }
        context.moveTo(startX, startY);
        context.lineTo(x, y);
        context.stroke();
        startX = x;
        startY = y;
    }
});
