#include <Printers.h>
#include "binary.h"       //defines buffer for packet
#include <XBee.h>         //defines xbee
#include <SoftwareSerial.h>
#define XBeeSerial Serial
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();

// Roomba Create2 connection

int rxPin=10;
int txPin=11;
int ddPin=5;
SoftwareSerial Roomba(rxPin,txPin);
bool poll = false;   // whether or not to run the poll Function
uint8_t sensors[20];

//-------------------------------------------------
void setup(){
  Roomba.begin(19200);       // Start Roomba Serial connection
  XBeeSerial.begin(19200);
  delay(1);
  xbee.begin(XBeeSerial);    // Start XBee Serial connection
  pinMode(ddPin,OUTPUT);     // Pin for waking up Roomba
  delay(200);
}

void loop(){

}

void wakeUp (void)
{
  digitalWrite(ddPin, HIGH);
  delay(100);
  digitalWrite(ddPin, LOW);
  delay(500);
  digitalWrite(ddPin, HIGH);
  delay(2000);
}

void startSafe()
{
  Roomba.write(128);  //Start
  delay(100);
  Roomba.write(131);  //Safe mode
  delay(1000);
}

//incoming data structure must be <id><len><data>

/*
IDTYPES
140 - Send Directly to attached
141 - Wake
142 - Poll
*/

  Buffer b(rx.getData(),rx.getDataLength());

  uint8_t id = b.remote()
  uint8_t len = b.remove<uint8_t>();
  uint8_t data [len]
  for(int i=0; i<=len;i++){
    data[i] = b.remove<uint8_t>();
  }
  if(id == 140){
    //SEND TO SERIAL
  } else if (id == 141){
    wakeUp();
  } else if (id == 142){
    //set_poll(len, data)
  } else {
    //raise error
  }
}
