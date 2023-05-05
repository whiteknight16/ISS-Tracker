import requests
import datetime
import geocoder
import smtplib
import credentials

MY_LAT=51.507351
MY_LONG=-0.127758

# ISS POSITION
def is_overhead():
    response=requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data=response.json()["iss_position"]
    iss_latitude=float(data["latitude"])
    iss_longitude=float(data["longitude"])

    if MY_LAT-5<=iss_latitude <=MY_LAT+5 and MY_LONG-5<=iss_longitude<=MY_LONG+5:
           return True


parameters={
    "lat":MY_LAT,
    "lng":MY_LONG,
    "formatted":0
}

# SUNRISE AND SUNSET
def is_night():       


    response=requests.get(f" https://api.sunrise-sunset.org/json",params=parameters).json()["results"]["sunrise"].split("T")[1].split(":")[0]
    response.raise_for_status()
    sunrise=int (response.json()["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int (response.json()["results"]["sunset"].split("T")[1].split(":")[0])
    time_now=datetime.datetime.now()

    if (time_now.hour>sunset or time_now.hour<sunrise):
          return True
    
if is_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
                    connection.starttls()
                    connection.login(user=credentials.my_mail,password=credentials.password)
                    connection.sendmail(from_addr=credentials.my_mail,to_addrs=credentials.my_mail,msg=f"Subject:Look Up\n\n You can see ISS")
                    connection.close()