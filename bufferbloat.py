from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.clean import cleanup

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

from monitor import monitor_qlen

import sys
import os
import math

parser = ArgumentParser(description="Bufferbloat tests")
parser.add_argument('--bw-host', '-B',
                    type=float,
                    help="Bandwidth of host links (Mb/s)",
                    default=1000)

parser.add_argument('--bw-net', '-b',
                    type=float,
                    help="Bandwidth of bottleneck (network) link (Mb/s)",
                    required=True)

parser.add_argument('--delay',
                    type=float,
                    help="Link propagation delay (ms)",
                    required=True)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    required=True)

parser.add_argument('--time', '-t',
                    help="Duration (sec) to run the experiment",
                    type=int,
                    default=10)

parser.add_argument('--maxq',
                    type=int,
                    help="Max buffer size of network interface in packets",
                    default=100)

# Linux uses CUBIC-TCP by default that doesn't have the usual sawtooth
# behaviour.  For those who are curious, invoke this script with
# --cong cubic and see what happens...
# sysctl -a | grep cong should list some interesting parameters.
parser.add_argument('--cong',
                    help="Congestion control algorithm to use",
                    default="reno")

# Expt parameters
args = parser.parse_args()

class BBTopo(Topo):
    "Simple topology for bufferbloat experiment."

    def build(self, n=2):
        first_host = self.addHost('h1')
        second_host = self.addHost('h2')
        
        switch = self.addSwitch('s0')

        # 1 Gbps link
        self.addLink(first_host, switch, bw=1000, delay='10ms')
        self.addLink(switch, second_host, bw=1.5, delay='10ms', max_queue_size=20)

# Simple wrappers around monitoring utilities.  You are welcome to
# contribute neatly written (using classes) monitoring scripts for
# Mininet!

def start_iperf(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    h2.cmd('iperf -s &')
    h1.cmd(f'iperf -c {h2.IP()} -t 1000 &')
    h1.cmd(f'ping -i 0.1 -c 100 {h2.IP()} & >> ping_output')
    h1.cmd('python3 -m http.server 80 &')

def start_qmon(iface, interval_sec=0.1, outfile="q.txt"):
    monitor = Process(target=monitor_qlen,
                      args=(iface, interval_sec, outfile))
    monitor.start()
    return monitor

def start_ping(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    ping_cmd = f"ping -i 0.1 -c {args.time * 10} {h2.IP()} > {args.dir}/ping.txt"
    h1.popen(ping_cmd, shell=True)

def start_webserver(net):
    h1 = net.get('h1')
    proc = h1.popen("python webserver.py", shell=True)
    sleep(1)
    return [proc]

def bufferbloat():
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    os.system("sysctl -w net.ipv4.tcp_congestion_control=%s" % args.cong)

    cleanup()
    
    topo = BBTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)
    net.pingAll()

    qmon = start_qmon(iface='s0-eth2', outfile='%s/q.txt' % (args.dir))
    start_iperf(net)
    start_ping(net)
    start_webserver(net)
    
    start_time = time()
    while True:
        sleep(5)
        now = time()
        delta = now - start_time
        if delta > args.time:
            break
        print("%.1fs left..." % (args.time - delta))

        h1 = net.get('h1')
        h2 = net.get('h2')
        for _ in range(3):
            h2.cmd(f'curl -o /dev/null -s -w "%{{time_total}}\\n" http://{h1.IP()}:80/index.html >> download_times')
            sleep(5)

    CLI(net)

    if qmon is not None:
        qmon.terminate()
    net.stop()
    
    # Ensure that all processes you create within Mininet are killed.
    # Sometimes they require manual killing.
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    bufferbloat()