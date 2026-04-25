// информация которая будет выводится на экране m5stick plus 2 
var display = require("display");
var wifi = require("wifi");
var keyboard = require("keyboard");

//вводим данные  о нашей wifi сети
var PC_IP = "192.168.1.20"; // IP нашего пк 
var PC_PORT = 8080; // порт который использует стик для подключения к пк
var WIFI_SSID = "Orange_Swiatlowod_C990"; // названия нашей wifi сети 
var WIFI_PASS = "HX5JDZLL5RNC"; // пароль от wifi 
// до сюда

var black = display.color(0, 0, 0);  // цвет дисплей фона нашего стика
var white = display.color(255, 255, 255);
// очищает весь экран на нашем стике и делает его простым и понятным
function drawUI(status) {
  display.fill(black);
  display.setTextSize(2);
  display.setTextColor(white);
  display.drawString("PC Control", 10, 10);
  display.setTextSize(1);
  display.drawString("A=Shutdown B=Reboot", 10, 50);
  display.drawString(status, 10, 80);
}
// на дисплее пишется о том что мы подключаемся к wifi
function sendCommand(cmd) {
  drawUI("Connecting WiFi...");

  if (!wifi.connected()) {
    wifi.connect(WIFI_SSID, 10, WIFI_PASS);
  }

  if (!wifi.connected()) {
    drawUI("WiFi Error!"); // пишет о том что у нас появились проблемы к подключению wifi не правильно веден пароль либо названия сети
    delay(2000);
    drawUI("Ready");
    return;
  }

  drawUI("Sending " + cmd + "...");
//команда для выключения пк которакя водится через cmd 
  var res = wifi.httpFetch(
    "http://" + PC_IP + ":" + PC_PORT + "/" + cmd,
    { method: "GET" }
  );

  if (res && res.body) {
    drawUI("Done: " + cmd);
  } else {
    drawUI("HTTP Error!"); // пишет о том что мы не смогли подключится к основной сети передакчи инфомации через инет HTTP
  }

  delay(2000);
  drawUI("Ready");
}

drawUI("Ready");
// выключает пк
while (true) {
  if (keyboard.getPrevPress()) {
    sendCommand("shutdown");
  }
  if (keyboard.getNextPress()) {
    sendCommand("reboot");
  }
  delay(50);
}
