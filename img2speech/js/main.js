const model_ver = [
    "a0.0.1",
    "b0.0.1"
]
let conf = ["off", 2000, 500, "off",100,50,50,model_ver.length-1];
function search_text(){
    var weblio = document.getElementById('weblio');
    weblio.src = "https://ejje.weblio.jp/content/"+text+"#summary"
}

t = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

window.onload = function () {
    let model_ver_select = document.getElementById("model_ver");
    let sdrtime = document.getElementById('sdr-time-result');
    let sdrspeed = document.getElementById('sdr-speed-result');
    let sdrspeech1 = document.getElementById('sdr-speech1-result');
    let sdrspeech2 = document.getElementById('sdr-speech2-result');
    let sdrspeech3 = document.getElementById('sdr-speech3-result');
    slidertime = document.getElementById('sdr-time');
    let sliderspeed = document.getElementById('sdr-speed');
    let sliderspeech1 = document.getElementById("sdr-speech1");
    let sliderspeech2 = document.getElementById("sdr-speech2");
    let sliderspeech3 = document.getElementById("sdr-speech3");
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    document.body.classList.remove('dark-theme');
    document.body.classList.add('light-theme');
    let ok = 0;
    const cookies = document.cookie; //全てのcookieを取り出して
    const cookiesArray = cookies.split('; '); // ;で分割し配列に


    for (const c of cookiesArray) { //一つ一つ取り出して
        const cArray = c.split('='); //さらに=で分割して配列に
        if (cArray[0] === 'dark') { // 取り出したいkeyと合致したら
            ok = 1;
            const btn = document.getElementById("btn-mode");
            if (cArray[1] === "1") {
                // ダークモード
                conf[0] = "on";
                document.body.classList.remove("light-theme");
                document.body.classList.add("dark-theme");
                btn.checked = true;
            } else {
                // ライトモード
                document.body.classList.remove("dark-theme");
                document.body.classList.add("light-theme");
                btn.checked = false;
            }
        } else if (cArray[0] === "slider_time_value") {
            slidertime.value = cArray[1]
            conf[1] = cArray[1];
        } else if (cArray[0] === "slider_speed_value") {
            sliderspeed.value = cArray[1]
            conf[2] = cArray[1];
        } else if (cArray[0] === "notice"){
            const btn2 = document.getElementById("btn-notice");
            btn2.checked = true;
            conf[3] = cArray[1];
        } else if (cArray[0] === "speech1"){
            sliderspeech1.value = cArray[1];
            conf[4] = cArray[1];
        } else if (cArray[0] === "speech2"){
            sliderspeech2.value = cArray[1];
            conf[5] = cArray[1];
        } else if (cArray[0] === "speech3"){
            sliderspeech3.value = cArray[1];
            conf[6] = cArray[1];
        } else if (cArray[0] === "model_ver"){
            model_ver_select.selectedIndex = cArray[1];
            conf[7] = cArray[1];
        }
    }
    if (ok === 0) {
        document.cookie = "dark=0";
        document.cookie = "slider_time_value=2000";
        document.cookie = "slider_speed_value=500";
        document.cookie = "notice="+conf[3]
        document.cookie = "speech1=100";
        document.cookie = "speech2=50";
        document.cookie = "speech3=50";
        document.cookie = "model_ver="+model_ver.length-1;

        darkModeMediaQuery.addListener((e) => {
            const darkModeOn = e.matches;
            if (darkModeOn) { // Dark
                document.cookie = "dark=1";
                conf[0] = "on";
            }
        });
        location.reload();
    } else {
        show_msg("info", "cookieデータから前回の設定を反映しました。<br>ダークモード:" + conf[0] + "" +
            "<br>文字起こしをする速度:"+conf[1]+"ms<br>文字認識をする速度:"+conf[2]+"ms<br>文字起こしの時に通知を出すか:"+conf[3]+
        "<br>発音時の音量:"+conf[4]+"%<br>発音時の発音速度:"+conf[5]+"%<br>発音時の音程:"+conf[6]+"%");
    }

    const btn1 = document.getElementById("btn-mode");
    const btn2 = document.getElementById("btn-notice");

    btn1.addEventListener("change", () => {
        if (btn1.checked === true) {
            // ダークモード
            document.cookie = "dark=1";
            show_msg("ok", "ダークモードにしました。<br><p style='color:red;'>※設定はリロードしてから反映されます。</p>")
        } else {
            // ライトモード
            document.cookie = "dark=0";
            show_msg("ok", "ライトモードにしました。<br><p style='color:red;'>※設定はリロードしてから反映されます。</p>")
        }
    });

    btn2.addEventListener("change", () => {
        if (btn2.checked === true) {
            document.cookie = "notice=on";
            conf[3] = "on";
            show_msg("ok", "文字起こしの時に通知を出すようにしました。")
        } else {
            document.cookie = "notice=off";
            conf[3] = "off";
            show_msg("ok", "文字起こしの時に通知を出さないようにしました。")
        }
    });
    setInterval(AI, sliderspeed.value);
    sdrtime.innerHTML = slidertime.value+"ms"
    sdrspeed.innerHTML = sliderspeed.value+"ms"
    sdrspeech1.innerHTML = sliderspeech1.value+"%"
    sdrspeech2.innerHTML = sliderspeech2.value+"%"
    sdrspeech3.innerHTML = sliderspeech3.value+"%"
    slidertime.addEventListener('input', (e) => {
        sdrtime.innerHTML = e.target.value+"ms";
        document.cookie = "slider_time_value="+e.target.value;
    });

    sliderspeed.addEventListener('input', (e) => {
        sdrspeed.innerHTML = e.target.value+"ms";
        document.cookie = "slider_speed_value="+e.target.value;
    });

    sliderspeech1.addEventListener('input', (e) => {
        sdrspeech1.innerHTML = sliderspeech1.value+"%";
        document.cookie = "speech1="+e.target.value;
        conf[4] = e.target.value
    });

    sliderspeech2.addEventListener('input', (e) => {
        sdrspeech2.innerHTML = sliderspeech2.value+"%";
        document.cookie = "speech2="+e.target.value;
        conf[5] = e.target.value
    });

    sliderspeech3.addEventListener('input', (e) => {
        sdrspeech3.innerHTML = sliderspeech3.value+"%";
        document.cookie = "speech3="+e.target.value;
        conf[6] = e.target.value
    });

    model_ver_select.addEventListener("change", (e) => {
        document.cookie = "model_ver="+e.target.selectedIndex;
    })
}

