import pandas as pd 
from influxdb import InfluxDBClient

client = InfluxDBClient(host="localhost", port=8086)
client.switch_database('<your-database>')

df = pd.read_csv("<your-csv file")
df.dropna(inplace=True)
print(df.shape)


for row_prikey, row in df.iloc[1:].iterrows():
    json_body=[{
        "measurement": "Test-data-Measurement",
        "tags": {"test_tag":row[0]},
        "fields":{
            "name":row[0],
            "country":row[1],
            "latitude":row[2],
            "longitude":row[3],
            "metric":row[4]
        }
    }]
    client.write_points(json_body)
    print("done")
