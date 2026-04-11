import base64
import json

# ─── FIXED CREDENTIALS ────────────────────────────────────────────────────────
UUID         = "9c5adfa3-2920-49dd-9fef-9d2272922110"
TROJAN_PASS  = "Infinity"
SS_PASS      = "Limitless"
SS_METHOD    = "chacha20-ietf-poly1305"

WS_PATHS = {
    "vless"   : "/gojo/domain/expansion",
    "vmess"   : "/gojo/hollow_technique/combine",
    "trojan"  : "/gojo/infinite/six_eyes",
    "ss"      : "/gojo/cursed_technique/combine",
}

# ─── GENERATORS ───────────────────────────────────────────────────────────────

def gen_vless(host: str) -> str:
    path = WS_PATHS["vless"]
    params = (
        f"encryption=none"
        f"&security=tls"
        f"&sni={host}"
        f"&type=ws"
        f"&host={host}"
        f"&path={path}"
    )
    return f"vless://{UUID}@{host}:443?{params}#Gojo-VLESS"


def gen_vmess(host: str) -> str:
    path = WS_PATHS["vmess"]
    config = {
        "v"    : "2",
        "ps"   : "Gojo-VMess",
        "add"  : host,
        "port" : "443",
        "id"   : UUID,
        "aid"  : "0",
        "scy"  : "auto",
        "net"  : "ws",
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


def gen_trojan(host: str) -> str:
    path = WS_PATHS["trojan"]
    params = (
        f"security=tls"
        f"&sni={host}"
        f"&type=ws"
        f"&host={host}"
        f"&path={path}"
    )
    return f"trojan://{TROJAN_PASS}@{host}:443?{params}#Gojo-Trojan"


def gen_ss(host: str) -> str:
    path = WS_PATHS["ss"]
    userinfo = base64.b64encode(f"{SS_METHOD}:{SS_PASS}".encode()).decode()
    params = (
        f"plugin=v2ray-plugin"
        f"&plugin-opts=server;tls;host={host};path={path}"
    )
    return f"ss://{userinfo}@{host}:443?{params}#Gojo-SS"


# ─── MAIN GENERATOR ───────────────────────────────────────────────────────────

def generate_all(cloud_run_url: str) -> dict:
    """
    Input  : full Cloud Run URL (e.g. https://gojo-proxy-xxxx-uc.a.run.app)
    Output : dict of all protocol links
    """
    # strip protocol prefix
    host = cloud_run_url.replace("https://", "").replace("http://", "").rstrip("/")

    return {
        "host"   : host,
        "vless"  : gen_vless(host),
        "vmess"  : gen_vmess(host),
        "trojan" : gen_trojan(host),
        "ss"     : gen_ss(host),
    }


# ─── FORMAT OUTPUT ────────────────────────────────────────────────────────────

def format_message(cloud_run_url: str) -> str:
    configs = generate_all(cloud_run_url)
    host    = configs["host"]

    msg = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔵 GOJO PROXY CONFIGS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 Host: `{host}`\n\n"

        f"⚡ VLESS+WS+TLS\n"
        f"`{configs['vless']}`\n\n"

        f"🟡 VMess+WS+TLS\n"
        f"`{configs['vmess']}`\n\n"

        f"🔴 Trojan+WS+TLS\n"
        f"`{configs['trojan']}`\n\n"

        f"🟢 Shadowsocks+WS+TLS\n"
        f"`{configs['ss']}`\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Tap any config to copy"
    )
    return msg


# ─── TEST ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_url = "https://gojo-proxy-abcd1234-uc.a.run.app"
    print(format_message(test_url))
