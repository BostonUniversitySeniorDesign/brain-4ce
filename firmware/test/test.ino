#include <DSPI.h>
#include <OpenBCI_32bit_Library.h>
#include <OpenBCI_32bit_Library_Definitions.h>

int bytesToInt(unsigned char *byte) {
  uint val = 0;

  unsigned char* byteAdrr = byte;

  for (int i = 0 ; i < 3 ; i++) {
    val = val | (int(*(byte+i)) << (i << 3));
  }

  return val;
}

void setup() {
  // Bring up the OpenBCI Board
  board.begin();
  // Don't use the accel
  board.useAccel(false);
}

void loop() {
  
  board.loop();

  if (board.streaming) {
    if (board.channelDataAvailable) {
      // Read from the ADS(s), store data, set channelDataAvailable flag to false
      board.updateChannelData();

      Serial.print("\n");

      for (int i = 0 ; i < 24 ; i += 3){
        Serial.printf("%08d\t",bytesToInt(&board.boardChannelDataRaw[i]));
      }
      delay(1000);
    }
  }
  // Check the serial ports for new data
  if (board.hasDataSerial0()) board.processChar(board.getCharSerial0());
  if (board.hasDataSerial1()) board.processChar(board.getCharSerial1());
}