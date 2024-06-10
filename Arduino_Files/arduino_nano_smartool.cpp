#include <Wire.h>
#include <SPI.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
// #include "Adafruit_MAX31855.h"

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
// Is for thermocouple (no longer used)
// #define MAXDO   16
// #define MAXCS   15
// #define MAXCLK  14

// initialize the Thermocouple
// Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

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
float lastInnerTemp = -100;
float lastPressure1 = 0;
float lastPressure2 = 0;
float lastClosingForce1 = 0;
float lastclosingForce2 = 0;
int timevar;

// double tempKistler1;

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

  Serial.print("Range = ");
  Serial.print(2 << lis.getRange());
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

  // MPU6050 (acceleration sensor)
  ////////////////////////////////////////////////////////////////////////
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);

  //mpu.setGyroRange(MPU6050_RANGE_500_DEG);


  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  //Serial.print("Filter bandwidth set to: ");

  // tool inner temperature
  analogReadResolution(12);

  Serial.println("");
  //delay(100);

  timevar = millis();
}

void loop() {
  // lis.read();      // get X Y and Z data at once
  // Then print out the raw data
  // Serial.print("X:  "); Serial.print(lis.x);
  // Serial.print("  \tY:  "); Serial.print(lis.y);
  // Serial.print("  \tZ:  "); Serial.print(lis.z);

  // tempKistler1 = thermocouple.readCelsius();

  // if (isnan(tempKistler1)) {
  //    uint8_t e = thermocouple.readError();
  //    if (e & MAX31855_FAULT_OPEN) tempKistler1 = -333;       //("FAULT: Thermocouple is open - no connections.");
  //    if (e & MAX31855_FAULT_SHORT_GND) tempKistler1 = -444;  //("FAULT: Thermocouple is short-circuited to GND.");
  //    if (e & MAX31855_FAULT_SHORT_VCC) tempKistler1 = -555;  //("FAULT: Thermocouple is short-circuited to VCC.");
  //  }

  /* Or....get a new sensor event, normalized */
  sensors_event_t event, a, g, temp, dht22;
  lis.getEvent(&event);
  mpu.getEvent(&a, &g, &temp);

  // Temperature and humidity every 2 seconds updated
  if (millis() - timevar > 2000) {
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

  // tool inner temperature every second
  if (millis() - timevar > 1000) {
    int KistlerTemp = analogRead(A0);
    float innerTemp = (KistlerTemp / 4095) * 400.0 ; //400°C ist der maximale Messbereich
    lastInnerTemp = innerTemp;
  }

  if (millis() - timevar > 1000) {
    int KistlerDruck1 = analogRead(A1);
    float innerPressure = (KistlerDruck1 / 4095) * 2000.0 ; // 2000 kPa ist der maximale Messbereich
    lastPressure1 = innerPressure;
  }

  if (millis() - timevar > 1000) {
    int KistlerDruck2 = analogRead(A2);
    float innerPressure = (KistlerDruck2 / 4095) * 2000.0 ; // 2000 kPa ist der maximale Messbereich
    lastPressure2 = innerPressure;
  }

  // max closing force is 100 kN
  if (millis() - timevar > 1000) {
    int Schließkraft1 = analogRead(A6);
    float closingForce = (Schließkraft1 / 4095) * 100.0 ; // 2000 kPa ist der maximale Messbereich
    lastClosingForce1 = closingForce;
  }

  // max closing force is 7 kN
  if (millis() - timevar > 1000) {
    int Schließkraft2 = analogRead(A7);
    float closingForce= (Schließkraft2 / 4095) * 7.0 ;
    lastClosingForce2 = closingForce;
  }

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("A");
  Serial.print(" ");
  Serial.print(event.acceleration.x);
  Serial.print(" ");
  Serial.print(event.acceleration.y);
  Serial.print(" ");
  Serial.print(event.acceleration.z);
  Serial.print(" ");
  Serial.print(a.acceleration.x);
  Serial.print(" ");
  Serial.print(a.acceleration.y);
  Serial.print(" ");
  Serial.print(a.acceleration.z);
  Serial.print(" ");
  Serial.print(lastTemp);
  Serial.print(" ");
  Serial.print(lastHum);
  Serial.print(" ");
  Serial.print(lastInnerTemp);
  Serial.print(" ");
  Serial.print(lastPressure1);
  Serial.print(" ");
  Serial.print(lastPressure2);
  Serial.print(" ");
  Serial.print(lastClosingForce1);
  Serial.print(" ");
  Serial.print(lastClosingForce2);
  Serial.print(" ");
  Serial.print(millis());

  Serial.println("");

  // delay(200);
}
