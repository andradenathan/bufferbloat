use std::net::UdpSocket;
use std::time::Instant;
use quiche::{Config, ConnectionId};

fn main() -> Result<(), std::io::Error> {
    let socket = UdpSocket::bind("127.0.0.1:8080")?;
    println!("Server listening on 127.0.0.1:8080");

    let mut config = Config::new(quiche::PROTOCOL_VERSION).unwrap();
    config.verify_peer(false); 
    config.load_cert_chain_from_pem_file("cert.crt").unwrap();
    config.load_priv_key_from_pem_file("cert.key").unwrap();
    config.set_application_protos(b"\x05hq-29").unwrap();

    let mut buf = [0; 65535];

    loop {
        let (len, client_addr) = socket.recv_from(&mut buf)?;
        println!("Received {} bytes from {}", len, client_addr);

        let conn_id = ConnectionId::from_ref(&buf[..len]);
        let mut conn = quiche::accept(&conn_id, None, &mut config).unwrap();
        
        while let Ok(_) = conn.recv(&mut buf) {}
        
        let send_buf = b"Hello from QUIC server!";
        let written = conn.stream_send(0, send_buf, true).unwrap();

        let mut out = [0; 65535];
        if let Ok(send_len) = conn.send(&mut out) {
            socket.send_to(&out[..send_len], client_addr)?;
            println!("Sent {} bytes back to {}", written, client_addr);
        }
    }
}