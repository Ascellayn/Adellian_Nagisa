// Header is 7zXZ Compressed and contains Type.MikaRoll_Header
// Data is 7zXZ Compressed, Pickle'd and contains Type.MikaRoll_Data

struct MikaRoll {
    char Signature[8];
    u8 Version[3];
    u16 HeaderLength;
    char Reserved[3];
    char Header[HeaderLength];
    char Data[sizeof($) - $];
};

MikaRoll mikaroll @ 0x0;