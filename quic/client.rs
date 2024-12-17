use std::net::UdpSocket;
use std::time::Instant;
use quiche::{Config, ConnectionId};

fn main() -> Result<(), std::io::Error> {
    let socket = UdpSocket::bind("0.0.0.0:0")?;
    socket.connect("127.0.0.1:8080")?;
    println!("Client connected to server at 127.0.0.1:8080");

    // QUIC configuration
    let mut config = Config::new(quiche::PROTOCOL_VERSION).unwrap();
    config.verify_peer(false); // Disable cert verification for testing
    config.set_application_protos(b"\x05hq-29").unwrap();

    let conn_id = ConnectionId::from_ref(&[0; 16]);
    let mut conn = quiche::connect(None, &conn_id, &mut config).unwrap();

    let mut out = [0; 65535];

    // Perform QUIC handshake
    let send_len = conn.send(&mut out).unwrap();
    socket.send(&out[..send_len])?;
    println!("Sent handshake packet ({} bytes)", send_len);

    let mut buf = [0; 65535];

    // Process server response
    let len = socket.recv(&mut buf)?;
    conn.recv(&mut buf[..len])?;

    println!("Handshake complete. Sending data...");

    // Send data to the server
    let data = b"Hello from QUIC client!";
    conn.stream_send(0, data, true).unwrap();
    let send_len = conn.send(&mut out).unwrap();
    socket.send(&out[..send_len])?;
    println!("Sent {} bytes to server", send_len);

    // Wait for response
    let len = socket.recv(&mut buf)?;
    conn.recv(&mut buf[..len])?;
    println!("Received response from server: {}", String::from_utf8_lossy(&buf[..len]));

    Ok(())
}