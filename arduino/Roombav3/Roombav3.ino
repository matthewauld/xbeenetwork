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


int inByte = 0;         // incoming serial byte

//---------------------------------------------
void setup()
{

  Roomba.begin(19200);          //start xbee and roomba
  XBeeSerial.begin(9600);
  delay(1);

  xbee.begin(XBeeSerial); //assign serial to xbee


  pinMode(ddPin, OUTPUT);       //this pin can wake roomba
  delay(2000);
  wakeUp();                     //wakes the roomba if sleeping

  startSafe();                  //puts roomba into safe mode - should be handeled on server side eventually


}
//---------------------------------------------
void loop() {
  //Check xbee for packet and process if exists and is an rx packet. Ignore others
  xbee.readPacket();
  if (xbee.getResponse().isAvailable()) {

    if(xbee.getResponse().getApiId() ==  ZB_RX_RESPONSE) {

      xbee.getResponse().getZBRxResponse(rx);
      processRxPacket(rx);


    }
  }



  //check for data from roomba and process
  processRoomba();


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

void processRxPacket(ZBRxResponse& rx){
  Buffer b(rx.getData(),rx.getDataLength());

  uint8_t len = b.remove<uint8_t>();
  for(int i=0; i<=len;i++){

    uint8_t data;
    data = b.remove<uint8_t>();
    Roomba.write(data);


  }
}





void processRoomba(){
  if (Roomba.available()>0){
    uint8_t data_length; //length of the data packets
    uint8_t start_byte; // first byte of the packet
    uint8_t checksum; //checksum byte
    bool flag = false;
    while (flag == false){ //read data until you get a 19 byte
      uint8_t start_byte = Roomba.read();
      if (start_byte == 19){
        flag = true;
      }
    }
    data_length = Roomba.read(); //get the length of th packet
    uint8_t data[data_length]; //define the data packet
    Roomba.readBytes(data,data_length); //read the data packets
    checksum = Roomba.read();
    if (calculateChecksum(data,data_length,checksum)){ //if the checksum calculates properly, transmit
      int packet_length = (int) data_length;
      AllocBuffer<100> packet;
      ZBTxRequest txRequest;
      packet.append<uint8_t>(start_byte);
      packet.append<uint8_t>(data_length);
      for (int i; i<data_length; i++){
        packet.append<uint8_t>(data[i]);
      }
      packet.append<uint8_t>(checksum);

      txRequest.setAddress64(0x0000000000000000);
      txRequest.setPayload(packet.head,packet.len());
      xbee.send(txRequest);
    }

  }
}
bool calculateChecksum(uint8_t *data, uint8_t data_length, uint8_t checksum){
  uint8_t result = data_length;
  for (int i=0; i<data_length; i++){
    result += data[i];
  }
  result += checksum;
  result = result & 0xFF;
  if (result == 0){
    return true;
  } else {
    return false;
  }
}
