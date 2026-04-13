selector_to_html = {"a[href=\"#raspberry-pi-pico-2-w\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html\">Raspberry Pi Pico 2 W</a><a class=\"headerlink\" href=\"#raspberry-pi-pico-2-w\" title=\"Link to this heading\">\uf0c1</a></h2><p>The main processor. An RP2350-based board with onboard CYW43439 for WiFi and\nBluetooth. Runs the balance control loop, PIO-based quadrature decoding, and\nPigweed RPC over UART.</p>", "a[href=\"#pololu-d24v5f5-5v-buck-regulator\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://www.pololu.com/product/2843/resources\">Pololu D24V5F5 5V Buck Regulator</a><a class=\"headerlink\" href=\"#pololu-d24v5f5-5v-buck-regulator\" title=\"Link to this heading\">\uf0c1</a></h2><p>Fixed 5V, 500mA step-down regulator. Accepts 4\u201336V input \u2014 covers the full 2S\nLiPo range (6.6\u20138.4V). Feeds the Pico W VSYS pin to produce the 3.3V logic rail\nvia the Pico\u2019s internal regulator.</p>", "a[href=\"#motor-connector-pololu-5187\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://www.pololu.com/file/0J1487/pololu-micro-metal-gearmotors-rev-6-2.pdf\">Motor Connector (Pololu 5187)</a><a class=\"headerlink\" href=\"#motor-connector-pololu-5187\" title=\"Link to this heading\">\uf0c1</a></h2><p>50:1 HPCB 6V DC motor with 12 CPR encoder. The connector carries two motor wires\n(M1, M2), encoder power (VCC), two encoder channels (OUT A, OUT B), and ground.\nAt 4x quadrature decoding this gives 2400 counts/revolution.</p>", "a[href=\"#minimu-9-lsm6dso-lis3mdl\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://www.pololu.com/product/2862\">MinIMU-9 (LSM6DSO + LIS3MDL)</a><a class=\"headerlink\" href=\"#minimu-9-lsm6dso-lis3mdl\" title=\"Link to this heading\">\uf0c1</a></h2><p>6-DOF IMU (accelerometer + gyroscope) plus magnetometer in a single breakout.\nCommunicates over I2C (address configurable via SA0). Powered from the 3.3V\nrail. Used to measure tilt angle for the balance controller.</p>", "a[href=\"#pololu-m2t550-motoron-dual-motor-driver\"]": "<h2 class=\"tippy-header\" style=\"margin-top: 0;\"><a class=\"reference external\" href=\"https://www.pololu.com/product/5079\">Pololu M2T550 Motoron Dual Motor Driver</a><a class=\"headerlink\" href=\"#pololu-m2t550-motoron-dual-motor-driver\" title=\"Link to this heading\">\uf0c1</a></h2><p>Dual DC H-bridge motor driver controlled over I2C. Accepts 4.5\u201340V motor supply\n(VM), making it compatible with a 2S LiPo directly. Drives both drive motors.\nI2C address is configurable; default is 0x10.</p>", "a[href=\"#sbr-components\"]": "<h1 class=\"tippy-header\" style=\"margin-top: 0;\">SBR Components<a class=\"headerlink\" href=\"#sbr-components\" title=\"Link to this heading\">\uf0c1</a></h1><p>Reference photos and pin descriptions for the components used in the\nSelf-Balancing Robot.</p>"}
skip_classes = ["headerlink", "sd-stretched-link"]

window.onload = function () {
    for (const [select, tip_html] of Object.entries(selector_to_html)) {
        const links = document.querySelectorAll(` ${select}`);
        for (const link of links) {
            if (skip_classes.some(c => link.classList.contains(c))) {
                continue;
            }

            tippy(link, {
                content: tip_html,
                allowHTML: true,
                arrow: true,
                placement: 'auto-start', maxWidth: 500, interactive: false,

            });
        };
    };
    console.log("tippy tips loaded!");
};
