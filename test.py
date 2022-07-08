bufferHex = "2a 00 04 00 00 00 08 48 61 63 6b 54 65 73 74 00 00 00 00 d7 5a 37 ff 7d 5a 69 5a 4b af a5 8c a0 b4 d7 ff e6 af a0 69 3c 08 00"
buffer = bytes.fromhex(bufferHex)

bufferString = "".join(map(chr, buffer))


print(bufferString)


def editPacket (oldPacket):
    newPacket = ""
    newMessage = "Hello World!"

    newPacket += str(1 + 8 + 1 + len(newMessage))
    
    for i in range(8):
        newPacket += chr(oldPacket[i])

    newPacket += len(newMessage)

    newPacket += newMessage

    return newPacket.encode('ascii')

for byte in buffer:
    print(byte)