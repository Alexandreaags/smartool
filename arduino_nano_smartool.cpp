#include <Wire.h>
#include <SPI.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

// Digital pin connected to the DHT sensor 
#define DHTPIN 17
#define DHTTYPE DHT22
// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10

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
}

void loop() {
  // lis.read();      // get X Y and Z data at once
  // Then print out the raw data
  // Serial.print("X:  "); Serial.print(lis.x);
  // Serial.print("  \tY:  "); Serial.print(lis.y);
  // Serial.print("  \tZ:  "); Serial.print(lis.z);

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
  

  Serial.println("");

  // delay(200);
}