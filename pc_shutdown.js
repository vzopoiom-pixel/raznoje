var display = require("display");
var wifi = require("wifi");
var keyboard = require("keyboard");

//вводим данные  о нашей wifi сети
var PC_IP = "192.168.1.49";
var PC_PORT = 8080;
var WIFI_SSID = "Orange_Swiatlowod_C990";
var WIFI_PASS = "HX5JDZLL5RNC";
// до сюда

var black = display.color(0, 0, 0);
var white = display.color(255, 255, 255);

function drawUI(status) {
  display.fill(black);
  display.setTextSize(2);
  display.setTextColor(white);
  display.drawString("PC Control", 10, 10);
  display.setTextSize(1);
  display.drawString("A=Shutdown B=Reboot", 10, 50);
  display.drawString(status, 10, 80);
}

function sendCommand(cmd) {
  drawUI("Connecting WiFi...");

  if (!wifi.connected()) {
    wifi.connect(WIFI_SSID, 10, WIFI_PASS);
  }

  if (!wifi.connected()) {
    drawUI("WiFi Error!");
    delay(2000);
    drawUI("Ready");
    return;
  }

  drawUI("Sending " + cmd + "...");

  var res = wifi.httpFetch(
    "http://" + PC_IP + ":" + PC_PORT + "/" + cmd,
    { method: "GET" }
  );

  if (res && res.body) {
    drawUI("Done: " + cmd);
  } else {
    drawUI("HTTP Error!");
  }

  delay(2000);
  drawUI("Ready");
}

drawUI("Ready");

while (true) {
  if (keyboard.getPrevPress()) {
    sendCommand("shutdown");
  }
  if (keyboard.getNextPress()) {
    sendCommand("reboot");
  }
  delay(50);
}
