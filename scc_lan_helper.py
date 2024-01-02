import pydivert
import socket
import threading

discovery_reply = bytearray.fromhex("0d0000000841475f4c414e4d4d030203030d0000001553706c696e74657243656c6c355f50435f50524f44054e53070000000103030100000008cd56000000000000010000001011320000382c0813784c4a0110000000070000000207c0a8010705238f07000000000500010700000000050000010000000628d244d8d1ad010000001400000000000000000000000000000000000000000100000008cd56000000000000010000001011320000382c0813784c4a011000000002010c00070000000007000000020e0000000e53004b004900440052004f00570007000000000700000001070000001e07fffbfffd0007fffbfffc000700040010060000000007000400110007fffbfffe060000000207fffbffff0600000001070004000f06f0f747a5070004001506000000010700040013060000000207000400160600000000070004001a0671822bb607fffbfffb0007000400120600000001070004001b0600000000070004001c0600000000070004001d0600000000070004001e0600000000070004001f060000000007000400200600000000070004002106000000000700040022060000000007000400230600000000070004002406000000000700040025060000000007000400260600000000070004002706000000000700040028060000000007000400290600000000070004002a0600000000070004002b0600000000")
matchmaking_config = bytes.fromhex("485454502f312e3120323030204f4b0d0a43616368652d436f6e74726f6c3a20707269766174650d0a436f6e74656e742d547970653a20746578742f68746d6c3b20636861727365743d7574662d380d0a5365727665723a204d6963726f736f66742d4949532f31302e300d0a582d4173704e65742d56657273696f6e3a20322e302e35303732370d0a582d506f77657265642d42793a204153502e4e45540d0a446174653a204d6f6e2c203031204a616e20323032342032333a31303a303220474d540d0a436f6e74656e742d4c656e6774683a20313138330d0a0d0a3c524553504f4e534520786d6c6e733d22223e3c41757468656e7469636174696f6e5365727665723e3c56414c55453e6c622d61676f72612e756269736f66742e636f6d3a333038313c2f56414c55453e3c2f41757468656e7469636174696f6e5365727665723e3c4372656174654163636f756e743e3c56414c55453e68747470733a2f2f7365637572652e7562692e636f6d2f6c6f67696e2f437265617465557365722e617370783f6c616e673d25733c2f56414c55453e3c2f4372656174654163636f756e743e3c4c6f6262795365727665723e3c56414c55453e6c622d6c73672d70726f642e756269736f66742e636f6d3a333130353c2f56414c55453e3c2f4c6f6262795365727665723e3c4d6d705469746c6549643e3c56414c55453e3078413030343c2f56414c55453e3c2f4d6d705469746c6549643e3c53616e64626f7855726c3e3c56414c55453e70727564703a2f616464726573733d6c622d7264762d61732d70726f6430312e756269736f66742e636f6d3b706f72743d32333933313c2f56414c55453e3c2f53616e64626f7855726c3e3c53616e64626f7855726c57533e3c56414c55453e6e65312d7a332d61732d72647630332e756269736f66742e636f6d3a32333933303c2f56414c55453e3c2f53616e64626f7855726c57533e3c53657269616c4e616d653e3c56414c55453e53504c494e54455243454c4c3550433c2f56414c55453e3c2f53657269616c4e616d653e3c75706c61795f446f776e6c6f61645365727669636555726c3e3c56414c55453e68747470733a2f2f7365637572652e7562692e636f6d2f55706c617953657276696365732f55706c61794661636164652f446f776e6c6f6164536572766963657352455354584d4c2e7376632f524553542f584d4c2f3f75726c3d3c2f56414c55453e3c2f75706c61795f446f776e6c6f61645365727669636555726c3e3c75706c61795f44796e436f6e74656e744261736555726c3e3c56414c55453e687474703a2f2f737461746963382e63646e2e7562692e636f6d2f752f55706c61792f3c2f56414c55453e3c2f75706c61795f44796e436f6e74656e744261736555726c3e3c75706c61795f44796e436f6e74656e745365637572654261736555726c3e3c56414c55453e687474703a2f2f737461746963382e63646e2e7562692e636f6d2f3c2f56414c55453e3c2f75706c61795f44796e436f6e74656e745365637572654261736555726c3e3c75706c61795f5061636b6167654261736555726c3e3c56414c55453e687474703a2f2f737461746963382e63646e2e7562692e636f6d2f752f55706c61792f5061636b616765732f312e302e312f3c2f56414c55453e3c2f75706c61795f5061636b6167654261736555726c3e3c75706c61795f576562536572766963654261736555726c3e3c56414c55453e68747470733a2f2f7365637572652e7562692e636f6d2f55706c617953657276696365732f55706c61794661636164652f50726f66696c65536572766963657346616361646552455354584d4c2e7376632f524553542f3c2f56414c55453e3c2f75706c61795f576562536572766963654261736555726c3e3c2f524553504f4e53453e")

def packet_hook():
    with pydivert.WinDivert("udp.DstPort == 46000 and udp.PayloadLength == 510") as w:
        for packet in w:
            addr = packet.ipv4.src_addr
            print(f"Discovery reply [{packet.ipv4.src_addr}]")
            # Copy game ID
            discovery_reply[44:46] = packet.payload[44:46]
            # Copy peer ip address
            # Peer address not present in "bad" remote packet, so copy from the IPV4 layer directly
            discovery_reply[93:97] = socket.inet_aton(addr)
            packet.payload = bytes(discovery_reply)
            #forward the packet to the game
            w.send(packet)

if __name__ == "__main__":
    hook_thread = threading.Thread(target=packet_hook)
    hook_thread.start()
    sockserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockserv.bind(('0.0.0.0', 3074))
    sockserv.listen(10)
    while True:
        (sock, a) = sockserv.accept()
        print(f"MatchMakingConfig [{sock.getpeername()}], [{sock.recv(1024)}]")
        sock.sendall(matchmaking_config);
        sock.close()