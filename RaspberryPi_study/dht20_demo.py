import time
import seeed_dht

# for DHT10/20
sensor = seeed_dht.DHT("20",1) 
# sensor = seeed_dht.DHT("10") 
# for DHT11/DHT22
#sensor = seeed_dht.DHT("22", 12) 

print("DHT11 reading every second, Ctrl+C to quit")
try:
    while True:
        humi, temp = sensor.read()
        print(f"DHT11  Humidity {humi:.1f}%  Temperature {temp:.1f}°C")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nBye")
