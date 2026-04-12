import base64
import json

# ─── FIXED CREDENTIALS (gojo-8n1) ─────────────────────────────────────────────
UUID      = "91176cdd-217c-4073-969e-bfc10befc737"
SS_METHOD = "chacha20-ietf-poly1305"

BASE_PATH = "/gojo-8n1/real-multiplexer"

PATHS = {
    "vless_ws"  : f"{BASE_PATH}/vless-ws",
    "vless_hu"  : f"{BASE_PATH}/vless-hu",
    "vmess_ws"  : f"{BASE_PATH}/vmess-ws",
    "vmess_hu"  : f"{BASE_PATH}/vmess-hu",
    "trojan_ws" : f"{BASE_PATH}/trojan-ws",
    "trojan_hu" : f"{BASE_PATH}/trojan-hu",
    "ss_ws"     : f"{BASE_PATH}/ss-ws",
    "ss_hu"     : f"{BASE_PATH}/ss-hu",
}

# ─── GENERATORS ───────────────────────────────────────────────────────────────

def gen_vless(host, path, transport, tag):
    net = "ws" if transport == "ws" else "httpupgrade"
    params = (
        f"encryption=none"
        f"&security=tls"
        f"&sni={host}"
        f"&type={net}"
        f"&host={host}"
        f"&path={path}"
    )
    return f"vless://{UUID}@{host}:443?{params}#{tag}"


def gen_vmess(host, path, transport, tag):
    net = "ws" if transport == "ws" else "httpupgrade"
    config = {
        "v"    : "2",
        "ps"   : tag,
        "add"  : host,
        "port" : "443",
        "id"   : UUID,
        "aid"  : "0",
        "scy"  : "auto",
        "net"  : net,
        "type" : "none",
        "host" : host,
        "path" : path,
        "tls"  : "tls",
        "sni"  : host,
        "alpn" : "",
        "fp"   : "",
    }
    encoded = base64.b64encode(json.dumps(config).encode()).decode()
    return f"vmess://{encoded}"


def gen_trojan(host, path, transport, tag):
    net = "ws" if transport == "ws" else "httpupgrade"
    params = (
        f"security=tls"
        f"&sni={host}"
        f"&type={net}"
        f"&host={host}"
        f"&path={path}"
    )
    return f"trojan://{UUID}@{host}:443?{params}#{tag}"


def gen_ss(host, path, transport, tag):
    net = "ws" if transport == "ws" else "httpupgrade"
    userinfo = base64.b64encode(f"{SS_METHOD}:{UUID}".encode()).decode()
    params = (
        f"plugin=v2ray-plugin"
        f"&plugin-opts=server;tls;host={host};path={path}"
    )
    return f"ss://{userinfo}@{host}:443?{params}#{tag}"


# ─── FORMAT OUTPUT ────────────────────────────────────────────────────────────

def format_message(cloud_run_url: str) -> str:
    host = cloud_run_url.replace("https://", "").replace("http://", "").rstrip("/")

    configs = {
        "vless_ws"  : gen_vless(host,  PATHS["vless_ws"],  "ws",  "Gojo-VLESS-WS"),
        "vless_hu"  : gen_vless(host,  PATHS["vless_hu"],  "hu",  "Gojo-VLESS-HU"),
        "vmess_ws"  : gen_vmess(host,  PATHS["vmess_ws"],  "ws",  "Gojo-VMess-WS"),
        "vmess_hu"  : gen_vmess(host,  PATHS["vmess_hu"],  "hu",  "Gojo-VMess-HU"),
        "trojan_ws" : gen_trojan(host, PATHS["trojan_ws"], "ws",  "Gojo-Trojan-WS"),
        "trojan_hu" : gen_trojan(host, PATHS["trojan_hu"], "hu",  "Gojo-Trojan-HU"),
        "ss_ws"     : gen_ss(host,     PATHS["ss_ws"],     "ws",  "Gojo-SS-WS"),
        "ss_hu"     : gen_ss(host,     PATHS["ss_hu"],     "hu",  "Gojo-SS-HU"),
    }

    msg = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👁️ GOJO 8N1 CONFIGS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 `{host}`\n\n"

        f"⚡ VLESS+WS+TLS\n"
        f"`{configs['vless_ws']}`\n\n"

        f"⚡ VLESS+HU+TLS\n"
        f"`{configs['vless_hu']}`\n\n"

        f"🟡 VMess+WS+TLS\n"
        f"`{configs['vmess_ws']}`\n\n"

        f"🟡 VMess+HU+TLS\n"
        f"`{configs['vmess_hu']}`\n\n"

        f"🔴 Trojan+WS+TLS\n"
        f"`{configs['trojan_ws']}`\n\n"

        f"🔴 Trojan+HU+TLS\n"
        f"`{configs['trojan_hu']}`\n\n"

        f"🟢 SS+WS+TLS\n"
        f"`{configs['ss_ws']}`\n\n"

        f"🟢 SS+HU+TLS\n"
        f"`{configs['ss_hu']}`\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Tap any config to copy"
    )
    return msg


if __name__ == "__main__":
    test_url = "https://gojo-8n1-abcdef123456.us-central1.run.app"
    print(format_message(test_url))
