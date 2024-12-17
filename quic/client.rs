use std::net::{UdpSocket, SocketAddr};
use quiche::{self, Config, ConnectionId, RecvInfo};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let server_addr: SocketAddr = "127.0.0.1:4433".parse()?;
    let local_addr: SocketAddr = "0.0.0.0:0".parse()?; 

    let socket = UdpSocket::bind(local_addr)?;
    println!("Client connected from {}", socket.local_addr()?);
    
    let mut config = Config::new(quiche::PROTOCOL_VERSION)?;
    config
        .set_application_protos(&[b"\x05hq-29", b"\x08http/0.9"])
        .unwrap();
    config.set_max_idle_timeout(5000);
    config.set_initial_max_data(10_000_000);
    config.set_initial_max_stream_data_bidi_local(1_000_000);
    config.set_initial_max_streams_bidi(100);
    
    let conn_id = ConnectionId::from_ref(&[0xba; 16]);
    
    let mut conn = quiche::connect(
        Some("example.com"),
        &conn_id,
        local_addr,
        server_addr,
        &mut config,
    )?;
    println!("Connected to server {}", server_addr);
    
    let mut buf = [0; 65535];
    let mut out = [0; 65535];
    
    if let Ok((write, _)) = conn.send(&mut out) {
        socket.send_to(&out[..write], server_addr)?;
        println!("Sent {} bytes to server", write);
    }
    
    loop {   
        let (len, _) = socket.recv_from(&mut buf)?;
        println!("Received {} bytes from server", len);
        
        let recv_info = RecvInfo {
            from: server_addr,
            to: local_addr,
        };
        
        if let Ok(read) = conn.recv(&mut buf[..len], recv_info) {
            println!("Processed {} bytes from server", read);
        }
       
        if let Ok((write, _)) = conn.send(&mut out) {
            socket.send_to(&out[..write], server_addr)?;
            println!("Sent {} bytes to server", write);
        }
    }
}