importScripts("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs/dist/tf.min.js");
onmessage = async function (e) {
    if (e.data[0] === "loadmodel") {
        model = await tf.loadLayersModel("../model/" + e.data[1] + "/bin/model.json");
        postMessage("ok");
    } else {
        let inputTensor = tf.tensor(e.data);
        inputTensor = inputTensor.reshape([28, 28, 1])

        /* expand dimension (HWC ->  NHWC) */
        inputTensor = inputTensor.expandDims();
        let scores = model.predict(inputTensor).dataSync();
        const maxScoreIndex = tf.argMax(scores).arraySync();
        postMessage([maxScoreIndex, scores[maxScoreIndex]]);
    }
}