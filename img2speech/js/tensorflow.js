console.info(tf.version)

const thread = new Worker("js/predict.js");
thread.postMessage(["loadmodel", model_ver[conf[7]]]);
document.getElementById("load_msg").innerText = "必要なファイルをダウンロード中...(4.1MB/1分ほどかかる場合があります)"
thread.onmessage = (ret) => {
    if (ret.data === "ok") {
        $(function () { // 読み込み完了したら実行する
            $('#loader-bg').fadeOut(800);// ローディングを隠す
            $('#loader').fadeOut(300);
            $('#contens').css('display', 'block');// コンテンツを表示する
        });
    } else {
        maxScoreIndex = ret.data[0]
        let score = ret.data[1]

        /* Display result */
        // console.log(scores);
        document.getElementById("result-text").innerHTML = "<h3>" + t[maxScoreIndex] + " と認識中</h3> " +
            "<p class='border-bottom'>正答率:" + score.toFixed(3) * 100 + "%</p>" +
            "<br><p class='sentaku'>文字:<span id='text'>" + text + "</span></p>";
    }
}


function AI() {
    if (write === 1) {
        // console.log(model.input.shape);
        let MODEL_HEIGHT = 28;
        let MODEL_WIDTH = 28;
        try {

            /* Read image and convert into tensor */
            const img_org = document.getElementById('write');
            let inputTensor = tf.browser.fromPixels(img_org, 3);  // get rgb (without alpha)

            /* Resize to model input size (28x28) */
            inputTensor = inputTensor.resizeBilinear([MODEL_HEIGHT, MODEL_WIDTH])

            /* Convert to grayscale (keep dimension(HWC))*/
            inputTensor = inputTensor.mean(2, true);

            /* Reverse black and white */
            if (conf[0] === "off") inputTensor = tf.sub(255, inputTensor);

            /* Inference */
            // scores = model.execute(inputTensor, "output_scores");
            // console.log(Array.from(inputTensor.dataSync()))
            thread.postMessage(Array.from(inputTensor.dataSync()));
        } catch (e) {
            console.warn(e);
            show_msg("error", "内部エラーが発生しました。おそらくバグです。開発者にお知らせください。tensorflow.js<br>技術情報<br>" + e);
        }
    } else {
        document.getElementById("result-text").innerHTML = "<h3>書かれていません</h3> " +
            "<p class='border-bottom'>横の四角に文字を書いてください。</p>" +
            "<br><p class='sentaku'>文字:<span id='text'>" + text + "</span></p>";
    }
}