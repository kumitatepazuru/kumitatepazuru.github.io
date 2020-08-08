voices = window.speechSynthesis.getVoices();
console.debug(voices)
window.speechSynthesis.onvoiceschanged = () => {
    console.info("voice list reloaded.")
    voices = window.speechSynthesis.getVoices();
    console.info(voices)
};

function speech(text=null) {
    // 発話機能をインスタンス化
    var msg = new SpeechSynthesisUtterance();
    msg.voice = voices[1];
    msg.volume = conf[4]/100; // 音量 min 0 ~ max 1
    msg.rate = conf[5]/50; // 速度 min 0 ~ max 10
    msg.pitch = conf[6]/50; // 音程 min 0 ~ max 2
    if (text == null) {
        msg.text = document.getElementById("text").textContent; // 喋る内容
    } else {
        msg.text = text
    }
    msg.lang = 'en-US';

    // 発話実行
    speechSynthesis.speak(msg);
    show_msg("info","発音中...<br>"+msg.text)
}