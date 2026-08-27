import psutil

def get_listening_ports():
    results = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.status != psutil.CONN_LISTEN:
            continue

        try:
            process = psutil.Process(conn.pid) if conn.pid else None

            results.append({
                "port": conn.laddr.port,
                "address": conn.laddr.ip,
                "pid": conn.pid,
                "process": process.name() if process else "Unknown"
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            results.append({
                "port": conn.laddr.port,
                "address": conn.laddr.ip,
                "pid": conn.pid,
                "process": "Access Denied"
            })

    return sorted(results, key=lambda x: x["port"])


if __name__ == "__main__":
    for item in get_listening_ports():
        print(
            f"{item['address']}:{item['port']} "
            f"PID={item['pid']} "
            f"PROCESS={item['process']}"
        )
