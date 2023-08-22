// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  
  // Try to initialize!
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
}

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  //delay(1);
  /* Print out the values */
  //Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print("    ");
  //Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print("    ");
  //Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  //Serial.println(" m/s^2");

  //Serial.print("Rotation X: ");
  //Serial.print(g.gyro.x);
  //Serial.print(", Y: ");
  //Serial.print(g.gyro.y);
  //Serial.print(", Z: ");
  //Serial.print(g.gyro.z);
  //Serial.println(" rad/s");
//
  //Serial.print("Temperature: ");
  //Serial.print(temp.temperature);
  //Serial.println(" degC");

  Serial.println("");
  //delay(500);
}