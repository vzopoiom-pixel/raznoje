// Полный код для Arduino IDE (M5StickC Plus 2)
// Библиотеки: M5StickCPlus2, IRremote, WiFi, WebServer

#include <M5StickCPlus2.h>
#include <WiFi.h>
#include <WebServer.h>
#include <IRremote.h>
#include <HTTPClient.h>

// Конфигурация
const char* ssid = "Orange_Swiatlowod_C990"; //информация о назавания wifi
const char* password = "HX5JDZLL5RNC"; // пароль от wifi
WebServer server(80);

// IR передатчик (для управления телевизором)
#define IR_LED_PIN 9
IRsend irsend(IR_LED_PIN);

// Wake-on-LAN пакет для включения ПК
byte macPC[] = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55}; // MAC ПК

// Коды пульта Samsung TV (пример) можно еще добавить подбор ключей
#define TV_POWER 0xE0E040BF
#define TV_VOL_UP 0xE0E0E01F
#define TV_VOL_DOWN 0xE0E0D02F
#define TV_CH_UP 0xE0E048B7
#define TV_CH_DOWN 0xE0E008F7
#define TV_MUTE 0xE0E0F00F

class TVManager {
public:
    void sendIRCommand(uint32_t command) {
        irsend.sendSamsung(command, 32);
        Serial.println("IR команда отправлена");
    }
    
    void sendMessageToTV(String message) {
        // Использование DLNA/UPnP для отправки уведомления на Smart TV
        HTTPClient http;
        http.begin("http://[TV_IP]:7676/upnp/control/RenderingControl");
        http.addHeader("Content-Type", "text/xml; charset=\"utf-8\"");
        
        String body = "<?xml version=\"1.0\"?>"
                      "<s:Envelope s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">"
                      "<s:Body>"
                      "<u:SendString xmlns:u=\"urn:schemas-upnp-org:service:RenderingControl:1\">"
                      "<InstanceID>0</InstanceID>"
                      "<String>" + message + "</String>"
                      "</u:SendString>"
                      "</s:Body>"
                      "</s:Envelope>";
        
        int response = http.POST(body);
        if(response == 200) {
            Serial.println("Сообщение отправлено на TV"); // отправляет наше за рание подготовленое сообщение на телевизор
        } else {
            Serial.println("Ошибка отправки на TV"); // выдает ошибку если не получилось подключится/не правильно ведены данные
        }
        http.end(); // основной способ подключения 
    }
    
    void sendOSDMessage(String message) {
        // Альтернативный метод: через HDMI-CEC (требуется Shield)
        // Код для CEC (через I2C)
        Wire.beginTransmission(0x40); // CEC адрес
        Wire.write("tx 44 82 00 00 "); // Команда OSD сообщение
        for(int i = 0; i < message.length(); i++) {
            Wire.write(message[i]);
        }
        Wire.endTransmission();
    }
};

class PCManager {
public:
    void sendWakeOnLan() {
        // Формирование WOL пакета
        byte packet[102];
        for(int i = 0; i < 6; i++) packet[i] = 0xFF;
        for(int i = 6; i < 102; i += 6) {
            memcpy(packet + i, macPC, 6);
        }
        
        // Отправка через UDP
        WiFiUDP udp;
        udp.beginPacket(IPAddress(255, 255, 255, 255), 9);
        udp.write(packet, 102);
        udp.endPacket();
        Serial.println("Wake-on-LAN отправлен");
    }
    
    void sendShutdownCommand(String pc_ip) {
        // Удалённое выключение ПК (требует SSH или RPC)
        HTTPClient http;
        http.begin("http://" + pc_ip + ":8080/shutdown");
        http.POST("{\"command\":\"shutdown\"}");
        http.end();
    }
    
    void lockPC(String pc_ip) {
        // Блокировка ПК через Win+L
        HTTPClient http;
        http.begin("http://" + pc_ip + ":8080/lock");
        http.POST("");
        http.end();
    }
};
// внизу поданы команды которые мы сможем использовать для того чтобы контроливать пк и телевизор 
class DisplayManager {
public:
    void showMenu() {
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setTextColor(WHITE, BLACK);
        M5.Lcd.setTextSize(2);
        M5.Lcd.setCursor(0, 10);
        M5.Lcd.println("=== REMOTE CONTROL ===");
        M5.Lcd.println("BtnA: TV Power");
        M5.Lcd.println("BtnB: PC On");
        M5.Lcd.println("BtnC: Menu");
        M5.Lcd.println("Up: Vol+");
        M5.Lcd.println("Down: Vol-");
        M5.Lcd.println("Left: CH-");
        M5.Lcd.println("Right: CH+");
    }
    
    void showMessageInput(String message) {
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setCursor(0, 10);
        M5.Lcd.println("Message to TV:");
        M5.Lcd.println(message);
        M5.Lcd.println("Press C to send");
    }
    
    void showStatus(String status) {
        M5.Lcd.fillRect(0, 100, 240, 40, BLACK);
        M5.Lcd.setCursor(0, 110);
        M5.Lcd.setTextColor(GREEN);
        M5.Lcd.println(status);
        delay(1000);
        showMenu();
    }
};

// Глобальные объекты
TVManager tv;
PCManager pc;
DisplayManager display;

String messageBuffer = "";
bool inputMode = false;

void setupWebServer() {
    server.on("/", []() {
        String html = "<!DOCTYPE html><html><head><title>M5Stick Remote</title></head><body>";
        html += "<h1>M5StickC Plus 2 Remote</h1>";
        html += "<button onclick='fetch(\"/tv_power\")'>TV Power</button>";
        html += "<button onclick='fetch(\"/pc_on\")'>PC Wake</button>";
        html += "<button onclick='fetch(\"/tv_message\")'>Send Message</button>";
        html += "<form action='/sendmsg' method='POST'><input name='msg'><input type='submit'></form>";
        html += "</body></html>";
        server.send(200, "text/html", html);
    });
    
    server.on("/tv_power", []() {
        tv.sendIRCommand(TV_POWER);
        server.send(200, "text/plain", "TV Power Sent");
    });
    
    server.on("/pc_on", []() {
        pc.sendWakeOnLan();
        server.send(200, "text/plain", "WOL Sent");
    });
    
    server.on("/tv_message", []() {
        server.send(200, "text/html", "<form method='POST'><input name='msg'><input type='submit'></form>");
    });
    
    server.on("/sendmsg", HTTP_POST, []() {
        String msg = server.arg("msg");
        tv.sendMessageToTV(msg);
        server.send(200, "text/plain", "Message sent: " + msg);
    });
    
    server.begin();
}

void setup() {
    M5.begin();
    M5.Lcd.setRotation(1);
    M5.Lcd.setTextSize(2);
    
    Serial.begin(115200);
    
    // Подключение к WiFi
    WiFi.begin(ssid, password);
    while(WiFi.status() != WL_CONNECTED) {
        delay(500);
        M5.Lcd.print(".");
    }
    M5.Lcd.println("\nWiFi Connected!");
    M5.Lcd.println(WiFi.localIP());
    
    // Инициализация IR
    irsend.begin();
    
    setupWebServer();
    display.showMenu();
}

void loop() {
    M5.update();
    server.handleClient();
    
    // Обработка кнопок
    if(M5.BtnA.wasPressed()) {
        tv.sendIRCommand(TV_POWER);
        display.showStatus("TV Power Toggled");
    }
    
    if(M5.BtnB.wasPressed()) {
        pc.sendWakeOnLan();
        display.showStatus("WOL Sent to PC");
    }
    
    if(M5.BtnC.wasPressed()) {
        if(!inputMode) {
            inputMode = true;
            messageBuffer = "";
            display.showMessageInput(messageBuffer);
        } else {
            tv.sendMessageToTV(messageBuffer);
            display.showStatus("Message sent: " + messageBuffer);
            inputMode = false;
            display.showMenu();
        }
    }
    
    // Виртуальная клавиатура через акселерометр (наклон для ввода)
    if(inputMode) {
        float ax, ay, az;
        M5.Imu.getAccelData(&ax, &ay, &az);
        
        if(ay > 0.5) {
            messageBuffer += "A";
            display.showMessageInput(messageBuffer);
            delay(300);
        }
        if(ay < -0.5) {
            messageBuffer += "B";
            display.showMessageInput(messageBuffer);
            delay(300);
        }
        if(ax > 0.5) {
            messageBuffer += "C";
            display.showMessageInput(messageBuffer);
            delay(300);
        }
        if(ax < -0.5) {
            if(messageBuffer.length() > 0) {
                messageBuffer.remove(messageBuffer.length() - 1);
                display.showMessageInput(messageBuffer);
            }
            delay(300);
        }
    }
    
    // Жесты (тап по экрану)
    if(M5.Touch.getDetail()) {
        tv.sendOSDMessage("M5Stick Connected!");
        display.showStatus("Touch detected - OSD sent");
    }
    
    delay(100);
}
