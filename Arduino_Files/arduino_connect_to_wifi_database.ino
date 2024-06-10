/*
  Web client

 This sketch connects to a website (http://www.google.com)
 using the WiFi module.

 This example is written for a network using WPA encryption. For
 WEP or WPA, change the WiFi.begin() call accordingly.

 Circuit:
 * Board with NINA module (Arduino MKR WiFi 1010, MKR VIDOR 4000 and Uno WiFi Rev.2)

 created 13 July 2010
 by dlf (Metodo2 srl)
 modified 31 May 2012
 by Tom Igoe
 */

//////////////////////////////////////
// TEST VALUES
float data_1 = 132;
float data_2 = 4654.2;
float data_3 = 119;
float data_4 = 0.12;
float data_5 = 1;
float data_6 = 15;
float data_7 = 20;
float data_8 = 36;
float data_9 = 1.77;
float data_10 = 100;


#include <SPI.h>
#include <WiFiNINA.h>

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "tassito";        // your network SSID (name)
char pass[] = "tassiooo";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)
char server[] = "172.18.1.131";    // IPv4 ADRESS FOR NOTEBOOK WIFI NETWORK, NOT THE WIFI ROUTER!!!

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

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

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(server, 80)) {
    Serial.print("GET /testcode/arduino.php?data_1=");
    client.print("GET /testcode/arduino.php?data_1=");     //YOUR URL
    Serial.println(data_1);
    client.print(data_1);
    client.print("&data_2=");
    Serial.println("&data_2=");
    client.print(data_2);
    Serial.println(data_2);
    client.print("&data_3=");
    Serial.println("&data_3=");
    client.print(data_3);
    Serial.println(data_3);
    client.print("&data_4=");
    Serial.println("&data_4=");
    client.print(data_4);
    Serial.println(data_4);
    client.print("&data_5=");
    Serial.println("&data_5=");
    client.print(data_5);
    Serial.println(data_5);
    client.print("&data_6=");
    Serial.println("&data_6=");
    client.print(data_6);
    Serial.println(data_6);
    client.print("&data_7=");
    Serial.println("&data_7=");
    client.print(data_7);
    Serial.println(data_7);
    client.print("&data_8=");
    Serial.println("&data_8=");
    client.print(data_8);
    Serial.println(data_8);
    client.print("&data_9=");
    Serial.println("&data_9=");
    client.print(data_9);
    Serial.println(data_9);
    client.print("&data_10=");
    Serial.println("&data_10=");
    client.print(data_10);
    Serial.println(data_10);
    client.print(" ");      //SPACE BEFORE HTTP/1.1
    client.print("HTTP/1.1");
    client.println();
    client.println("Host: 192.168.137.1");
    client.println("Connection: close");
    client.println();
  }
}

void loop() {
  // if there are incoming bytes available
  // from the server, read them and print them:
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting from server.");
    client.stop();

    // do nothing forevermore:
    while (true);
  }
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
