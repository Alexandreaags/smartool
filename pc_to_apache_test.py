import requests
import logging

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
s.get('http://localhost/testcode/arduino.php?data_1=12&data_2=24&data_3=11&data_4=123&data_5=1234&data_6=1.2&data_7=125.4&data_8=112&data_9=12.22&data_10=12.22')
s.get('http://localhost/testcode/arduino.php?data_1=12&data_2=24&data_3=11&data_4=123&data_5=1234&data_6=1.2&data_7=125.4&data_8=112&data_9=12.22&data_10=12.22')
s.get('http://localhost/testcode/arduino.php?data_1=12&data_2=24&data_3=11&data_4=123&data_5=1234&data_6=1.2&data_7=125.4&data_8=112&data_9=12.22&data_10=12.22')
s.get('http://localhost/testcode/arduino.php?data_1=12&data_2=24&data_3=11&data_4=123&data_5=1234&data_6=1.2&data_7=125.4&data_8=112&data_9=12.22&data_10=12.22')
s.get('http://localhost/testcode/arduino.php?data_1=12&data_2=24&data_3=11&data_4=123&data_5=1234&data_6=1.2&data_7=125.4&data_8=112&data_9=12.22&data_10=12.22')



