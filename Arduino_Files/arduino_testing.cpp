#include <Wire.h>
#include <SPI.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include "Adafruit_MAX31855.h"
#include <WiFiNINA.h>

// Digital pin connected to the DHT sensor 
#define DHTPIN 17
#define DHTTYPE DHT22
// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10

// digital IO pins.
#define MAXDO   16
#define MAXCS   15
#define MAXCLK  14

// initialize the Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

// software SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);
// hardware SPI
//Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);
// I2C
Adafruit_LIS3DH lis = Adafruit_LIS3DH();

Adafruit_MPU6050 mpu;

DHT_Unified dht(DHTPIN, DHTTYPE);

float lastTemp = -100;
float lastHum = -100;
int timevar;

double tempKistler1;

int aux1, aux2;

// 
// ADDRESSING OF VARIABLES IN GET.SERIAL.MESSAGE ARRAY
// [0] = 'A' // CHARACTER USED TO KNOW WHEN A LINE STARTS ON TERMINAL
// [1] = ACC_LIS3DH X AXIS // M/S²
// [2] = ACC_LIS3DH Y AXIS // M/S²
// [3] = ACC_LIS3DH Z AXIS // M/S²
// [4] = ACC_MPU6050 X AXIS // M/S²
// [5] = ACC_MPU6050 Y AXIS // M/S²
// [6] = ACC_MPU6050 Z AXIS // M/S²
// [7] = DHT22 TEMPERATURE // °C
// [8] = DHT22 HUMIDITY // %
// [9] = KISTLER_1 TEMPERATURE // °C
//
//////////////////////////////////////////////////////////////////////
//                    WIFI CONNECTION
/////// ENTER WIFI SSID AND PASSWORD
char ssid[] = "tassito";     // your network SSID (name)
char pass[] = "tassiooo";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
char server[] = "192.168.137.1";    // IPv4 ADRESS FOR NOTEBOOK WIFI NETWORK, NOT THE WIFI ROUTER!!!

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;
//////////////////////////////////////////////////////////////////////

void setup(void) {
  // LIS3DH
  ////////////////////////////////////////////////////////////////////////////////////////////
  Serial.begin(115200);
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens

  dht.begin();

  Serial.println("LIS3DH test!");

  if (! lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    Serial.println("Couldnt start");
    while (1) yield();
  }
  Serial.println("LIS3DH found!");

  // lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!

  Serial.print("Range = "); Serial.print(2 << lis.getRange());
  Serial.println("G");

  // lis.setDataRate(LIS3DH_DATARATE_50_HZ);
  Serial.print("Data rate set to: ");
  switch (lis.getDataRate()) {
    case LIS3DH_DATARATE_1_HZ: Serial.println("1 Hz"); break;
    case LIS3DH_DATARATE_10_HZ: Serial.println("10 Hz"); break;
    case LIS3DH_DATARATE_25_HZ: Serial.println("25 Hz"); break;
    case LIS3DH_DATARATE_50_HZ: Serial.println("50 Hz"); break;
    case LIS3DH_DATARATE_100_HZ: Serial.println("100 Hz"); break;
    case LIS3DH_DATARATE_200_HZ: Serial.println("200 Hz"); break;
    case LIS3DH_DATARATE_400_HZ: Serial.println("400 Hz"); break;

    case LIS3DH_DATARATE_POWERDOWN: Serial.println("Powered Down"); break;
    case LIS3DH_DATARATE_LOWPOWER_5KHZ: Serial.println("5 Khz Low Power"); break;
    case LIS3DH_DATARATE_LOWPOWER_1K6HZ: Serial.println("16 Khz Low Power"); break;
  }
  // MPU6050
  ////////////////////////////////////////////////////////////////////////////////////////////
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  //mpu.setGyroRange(MPU6050_RANGE_500_DEG);


  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  //Serial.print("Filter bandwidth set to: ");
 

  Serial.println("");
  //delay(100);

  timevar = millis();

  /////////////////////////////////////////////////////////////
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();
}

void loop() {
  aux1 = millis();

  if (!client.connected()) {
    if (client.connect(server, 80)) {
      Serial.println("Conectado ao servidor");
    } else {
      Serial.println("Falha na conexão com o servidor");
      delay(5000);
      return;
    }
  }

  tempKistler1 = thermocouple.readCelsius();
  if (isnan(tempKistler1)) {
    uint8_t e = thermocouple.readError();
    if (e & MAX31855_FAULT_OPEN) tempKistler1 = -333;       //("FAULT: Thermocouple is open - no connections.");
    if (e & MAX31855_FAULT_SHORT_GND) tempKistler1 = -444;  //("FAULT: Thermocouple is short-circuited to GND.");
    if (e & MAX31855_FAULT_SHORT_VCC) tempKistler1 = -555;  //("FAULT: Thermocouple is short-circuited to VCC.");
  }
  /* Or....get a new sensor event, normalized */
  sensors_event_t event, a, g, temp, dht22;
  lis.getEvent(&event);
  mpu.getEvent(&a, &g, &temp);
  // Temperature and humidity
  if (millis() - timevar > 2000)
  {
    dht.temperature().getEvent(&dht22);
    if (isnan(dht22.temperature)) {
      lastTemp = -100;
    }
    else {
      lastTemp = dht22.temperature;
    }
    dht.humidity().getEvent(&dht22);
    if (isnan(dht22.relative_humidity)) {
      lastHum = -100;
    }
    else {
      lastHum = dht22.relative_humidity;
    }
    timevar = millis();
  }
  /////////////////////////
  //Serial.print("GET /testcode/arduino.php?data_1=");
  client.print("GET /testcode/arduino.php?data_1=");     //YOUR URL
  //Serial.println(event.acceleration.x);
  client.print(event.acceleration.x);
  client.print("&data_2=");
  //Serial.println("&data_2=");
  client.print(event.acceleration.y);
  //Serial.println(event.acceleration.y);
  client.print("&data_3=");
  //Serial.println("&data_3=");
  client.print(event.acceleration.z);
  //Serial.println(event.acceleration.z);
  client.print("&data_4=");
  //Serial.println("&data_4=");
  client.print(a.acceleration.x);
  //Serial.println(a.acceleration.x);
  client.print("&data_5=");
  //Serial.println("&data_5=");
  client.print(a.acceleration.y);
  //Serial.println(a.acceleration.y);
  client.print("&data_6=");
  //Serial.println("&data_6=");
  client.print(a.acceleration.z);
  //Serial.println(a.acceleration.z);
  client.print("&data_7=");
  //Serial.println("&data_7=");
  client.print(lastTemp);
  //Serial.println(lastTemp);
  client.print("&data_8=");
  //Serial.println("&data_8=");
  client.print(lastHum);
  //Serial.println(lastHum);
  client.print("&data_9=");
  //Serial.println("&data_9=");
  client.print(tempKistler1);
  //Serial.println(tempKistler1);
  client.print("&data_10=");
  //Serial.println("&data_10=");
  client.print(NULL);
  //Serial.println(NULL);
  client.print(" ");      //SPACE BEFORE HTTP/1.1
  client.print("HTTP/1.1");
  client.println();
  client.println("Host: 192.168.137.1");
  client.println("Connection: keep-alive");
  client.println();
  /////////////////////////
  //delay(100);
  aux1 = millis() - aux1;
  Serial.println(aux1);
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}