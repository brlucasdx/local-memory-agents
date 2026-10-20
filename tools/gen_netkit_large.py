"""Generate `netkit` 0.2.0: the 20 original fictional symbols plus 480 generated ones.

The generated symbols share the network-automation domain (some deliberately
close to the original 20) so finding the right API inside a ~20k-token
reference is a real retrieval problem. Deterministic (fixed seed): anyone can
regenerate the exact same package.
Usage: python3 -I tools/gen_netkit_large.py
"""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "packages/source/netkit-0.1/package.json"
OUT = ROOT / "packages/source/netkit-0.2/package.json"

PREFIXES = ["vrx", "lldp", "oui", "pfx", "ifx", "bgp", "ont", "cfg", "arp", "mtu", "acl", "trk", "sfp", "rt", "vrf",
            "snmp", "ntp", "lag", "poe", "stp", "ospf", "isis", "mpls", "qos", "dhcp", "dns", "nat", "ipsec", "vxlan",
            "evpn", "pim", "igmp", "vrrp", "bfd", "lacp", "mac", "fdb", "olt", "gpon", "syslog"]
VERBS = ["scan", "dump", "probe", "carve", "fold", "unfold", "canon", "diff", "audit", "sync", "trace", "peek", "tally",
         "purge", "pin", "drain", "warm", "seal", "split", "merge", "rank", "sweep", "snap", "lint", "map"]
OBJECTS = ["neighbors", "sessions", "counters", "prefixes", "interfaces", "routes", "timers", "members", "entries",
           "policies", "tunnels", "groups", "leases", "zones", "peers", "queues", "ports", "profiles", "tables", "alarms"]
ACTIONS = {
    "scan": "list the {o} of {p}", "dump": "return the raw {o} table of {p}", "probe": "test reachability of the {o} of {p}",
    "carve": "split the {o} of {p} into smaller blocks", "fold": "compress the {o} of {p} into a compact spec",
    "unfold": "expand a compact {p} {o} spec into a full list", "canon": "normalize the names of the {o} of {p}",
    "diff": "compare two snapshots of the {o} of {p}", "audit": "check the {o} of {p} against policy",
    "sync": "copy the {o} of {p} to the standby node", "trace": "follow the path of the {o} of {p}",
    "peek": "read one entry from the {o} of {p}", "tally": "count the {o} of {p} by state",
    "purge": "remove stale {o} from {p}", "pin": "make the {o} of {p} static", "drain": "move traffic away from the {o} of {p}",
    "warm": "pre-load the {o} of {p} into cache", "seal": "lock the {o} of {p} against changes",
    "split": "divide the {o} of {p} by VRF", "merge": "combine duplicate {o} of {p}", "rank": "sort the {o} of {p} by load",
    "sweep": "scan all devices for {p} {o}", "snap": "take a snapshot of the {o} of {p}", "lint": "validate the syntax of the {p} {o}",
    "map": "draw a map of the {o} of {p}",
}
SIGS = ["(device: str) -> list[dict]", "(device: str, name: str) -> dict", "(router: str) -> dict[str, int]",
        "(spec: str) -> list[int]", "(old: str, new: str) -> str", "(host: str, timeout: float = 2.0) -> bool",
        "(switch: str, vlan: int) -> list[str]", "(olt: str, onu_id: int) -> dict"]


def main() -> None:
    rng = random.Random(20261020)
    base = json.loads(BASE.read_text())
    taken = {s["name"] for s in base["symbols"]}
    generated = []
    while len(generated) < 480:
        p, v, o = rng.choice(PREFIXES), rng.choice(VERBS), rng.choice(OBJECTS)
        name = f"{p}_{v}" if rng.random() < 0.5 else f"{p}_{v}_{o[:4]}"
        if name in taken:
            continue
        taken.add(name)
        doc = ACTIONS[v].format(o=o, p=p.upper())
        generated.append({"name": name, "signature": rng.choice(SIGS), "doc": doc, "keys": [doc]})
    symbols = base["symbols"] + generated
    rng.shuffle(symbols)  # the 20 task symbols end up spread through the reference
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({**base, "version": "0.2.0",
                               "provenance": base["provenance"] + " Version 0.2.0 adds 480 generated decoy symbols (tools/gen_netkit_large.py, seed 20261020).",
                               "symbols": symbols}, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(symbols)} symbols -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
