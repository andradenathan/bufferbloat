use std::net::{UdpSocket, SocketAddr};
use quiche::{self, Config, ConnectionId, RecvInfo};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let server_addr: SocketAddr = "127.0.0.1:4433".parse()?;

    let socket = UdpSocket::bind(&server_addr)?;
    println!("Server listening on {}", server_addr);

    let mut config = Config::new(quiche::PROTOCOL_VERSION)?;
    config
        .set_application_protos(&[b"\x05hq-29", b"\x08http/0.9"])
        .unwrap();
    config.set_max_idle_timeout(5000);
    config.set_max_recv_udp_payload_size(65535);
    config.set_initial_max_data(10_000_000);
    config.set_initial_max_stream_data_bidi_local(1_000_000);
    config.set_initial_max_streams_bidi(100);

    let conn_id = ConnectionId::from_ref(&[0xba; 16]);

    let mut buf = [0; 65535];
    let mut out = [0; 65535];

    loop {
        let (len, client_addr) = socket.recv_from(&mut buf)?;
        println!("Received {} bytes from {}", len, client_addr);

        let mut conn = quiche::accept(
            &conn_id,
            None,
            server_addr,
            client_addr,
            &mut config,
        )?;

        let recv_info = RecvInfo {
            from: client_addr,
            to: server_addr,
        };

        if let Ok(read) = conn.recv(&mut buf[..len], recv_info) {
            println!("Processed {} bytes", read);
        }

        if let Ok((write, _)) = conn.send(&mut out) {
            socket.send_to(&out[..write], client_addr)?;
            println!("Sent {} bytes to {}", write, client_addr);
        }
    }
}