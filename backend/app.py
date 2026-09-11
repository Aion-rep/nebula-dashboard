import json
import os

from flask import Flask, jsonify
import mysql.connector
import redis

app = Flask(__name__)

DB = dict(
    host=os.getenv("DB_HOST", "mariadb"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "nebula"),
    user=os.getenv("DB_USER", "nebula"),
    password=os.getenv("DB_PASSWORD", "root_pass"),
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
TTL = int(os.getenv("CACHE_TTL", "30"))


def dbc():
    return mysql.connector.connect(**DB)


def rc():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )


@app.get("/health")
def health():
    ok = True
    out = {
        "status": "healthy",
        "database": "connected",
        "cache": "connected"
    }

    try:
        c = dbc()
        c.close()
    except Exception:
        ok = False
        out["database"] = "unavailable"

    try:
        rc().ping()
    except Exception:
        ok = False
        out["cache"] = "unavailable"

    out["status"] = "healthy" if ok else "degraded"

    return jsonify(out), 200 if ok else 503


@app.get("/api/dashboard")
def dashboard():
    r = rc()
    key = "nebula:dashboard"

    hit = r.get(key)

    if hit:
        d = json.loads(hit)
        d["cache"] = "HIT"
        return jsonify(d)

    c = dbc()
    cur = c.cursor(dictionary=True)

    # Total number of servers
    cur.execute("SELECT COUNT(*) count FROM servers")
    sc = cur.fetchone()["count"]

    # Total vCPU of ACTIVE servers
    cur.execute(
        "SELECT COALESCE(SUM(vcpu), 0) vcpu "
        "FROM servers WHERE state='ACTIVE'"
    )
    vc = int(cur.fetchone()["vcpu"])

    # Total networks
    cur.execute("SELECT COUNT(*) count FROM networks")
    nc = cur.fetchone()["count"]

    # Server details
    cur.execute(
        "SELECT id, name, region, state, flavor, ip, vcpu "
        "FROM servers ORDER BY id"
    )
    servers = cur.fetchall()

    # Region details
    cur.execute(
        "SELECT name, code, servers, utilization "
        "FROM regions ORDER BY id"
    )
    regions = cur.fetchall()

    # Convert MariaDB Decimal values to JSON-compatible floats
    for region in regions:
        region["utilization"] = float(region["utilization"])

    cur.close()
    c.close()

    d = {
        "kpis": {
            "servers": sc,
            "vcpu": vc,
            "storage": "72.6 TB",
            "networks": nc
        },
        "servers": servers,
        "regions": regions,
        "cache": "MISS"
    }

    r.setex(key, TTL, json.dumps(d))

    return jsonify(d)


@app.get("/api/redis")
def redis_status():
    r = rc()

    r.setex(
        "nebula:test",
        30,
        "Redis is working"
    )

    return jsonify(
        status="connected",
        value=r.get("nebula:test")
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
