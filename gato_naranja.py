import argparse
import concurrent.futures
import time
import urllib.request
import urllib.error
import ssl
import statistics

BANNER = """
 ⠀⠀⠀⢠⣾⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⠀⠀⣰⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⠀⢰⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⣀⣤⣤⣶⣾⣿⣿⣿⡷ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀ 
 ⣿⣿⣿⡇⠀⡾⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣧⡀⠁⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢹⠉⠙⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⣀⣼⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⠿⠋⢃⠈⠢⡁⠒⠄⡀⠈⠁⠀⠀⠀⠀⠀⠀⠀ 
 ⣿⣿⠟⠁⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠈⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 
 ɢᴀᴛᴏ ɴᴀʀᴀɴᴊᴀ
 ʙʏ ʜᴏʀɪ12_86 / ʀᴏᴏᴛꜱɪᴛᴇ
"""

def fetch(url, timeout):
    start = time.perf_counter()
    code = None
    ok = False
    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, timeout=timeout, context=context) as resp:
            code = resp.getcode()
            ok = 200 <= code < 400
            _ = resp.read(1)
    except Exception:
        ok = False
    latency = time.perf_counter() - start
    return ok, latency, code

def percentile(values, p):
    if not values:
        return 0.0
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round((p / 100.0) * (len(s) - 1)))))
    return s[k]

def run_test(url, total_requests, concurrency, timeout):
    latencies = []
    successes = 0
    failures = 0
    status_counts = {}
    start_total = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(fetch, url, timeout) for _ in range(total_requests)]
        for fut in concurrent.futures.as_completed(futures):
            ok, latency, code = fut.result()
            latencies.append(latency)
            if ok:
                successes += 1
            else:
                failures += 1
            status_counts[code] = status_counts.get(code, 0) + 1
    total_time = time.perf_counter() - start_total
    avg = statistics.mean(latencies) if latencies else 0.0
    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    p99 = percentile(latencies, 99)
    throughput = (len(latencies) / total_time) if total_time > 0 else 0.0
    success_rate = (successes / len(latencies)) * 100 if latencies else 0.0
    error_rate = (failures / len(latencies)) * 100 if latencies else 0.0
    return {
        "url": url,
        "requests": len(latencies),
        "concurrency": concurrency,
        "total_time_sec": total_time,
        "throughput_rps": throughput,
        "successes": successes,
        "failures": failures,
        "success_rate": success_rate,
        "error_rate": error_rate,
        "latency_avg_ms": avg * 1000,
        "latency_p50_ms": p50 * 1000,
        "latency_p95_ms": p95 * 1000,
        "latency_p99_ms": p99 * 1000,
        "status_counts": status_counts,
    }

def print_summary(s):
    print("Gato Naranja - Prueba de estrés HTTP")
    print(f"URL: {s['url']}")
    print(f"Solicitudes: {s['requests']} | Concurrencia: {s['concurrency']}")
    print(f"Tiempo total: {s['total_time_sec']:.3f} s | Rendimiento: {s['throughput_rps']:.2f} req/s")
    print(f"Éxitos: {s['successes']} | Fallos: {s['failures']}")
    print(f"Tasa de éxito: {s['success_rate']:.2f}% | Tasa de error: {s['error_rate']:.2f}%")
    print("Latencias (ms): avg={:.2f} p50={:.2f} p95={:.2f} p99={:.2f}".format(
        s['latency_avg_ms'], s['latency_p50_ms'], s['latency_p95_ms'], s['latency_p99_ms']
    ))
    print("Códigos de estado:")
    for code, count in sorted(s['status_counts'].items(), key=lambda x: (x[0] is None, x[0])):
        print(f"  {code}: {count}")

def main():
    parser = argparse.ArgumentParser(prog="Gato Naranja", description="Prueba de estrés simple para servidores HTTP")
    parser.add_argument("--url", help="URL objetivo")
    parser.add_argument("--target", help="IP/host o URL (auto)" )
    parser.add_argument("--ip", help="IP o host objetivo")
    parser.add_argument("--port", type=int, default=80, help="Puerto (por defecto 80)")
    parser.add_argument("--scheme", default="http", choices=["http", "https"], help="Esquema: http/https")
    parser.add_argument("--path", default="/", help="Ruta, por ejemplo /api")
    parser.add_argument("--requests", type=int, default=100, help="Número total de solicitudes")
    parser.add_argument("--concurrency", type=int, default=10, help="Nivel de concurrencia (hilos)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Tiempo de espera por solicitud (s)")
    args = parser.parse_args()

    print(BANNER)
    print("Gato Naranja")

    target_url = args.url
    if args.target:
        if args.target.startswith("http://") or args.target.startswith("https://"):
            target_url = args.target
        else:
            p = args.path if args.path.startswith("/") else "/" + args.path
            target_url = f"{args.scheme}://{args.target}:{args.port}{p}"
    if args.ip and not target_url:
        p = args.path if args.path.startswith("/") else "/" + args.path
        target_url = f"{args.scheme}://{args.ip}:{args.port}{p}"
    if not target_url:
        parser.error("Debe especificar --url, --ip o --target")

    summary = run_test(target_url, args.requests, args.concurrency, args.timeout)
    print_summary(summary)

if __name__ == "__main__":
    main()