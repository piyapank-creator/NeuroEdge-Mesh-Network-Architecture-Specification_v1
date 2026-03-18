"""
NeuroEdge Mesh Network Simulator v1.2
CP352005 Networks - NeuroEdge Mesh Network Architecture

NEW in v1.2:
  - CLOUD_02 backup node (eliminates CLOUD SPOF)
  - Node failure simulation: click any node on canvas to toggle ON/OFF
  - Auto-fallback: if primary destination is DOWN, reroute to backup CLOUD
  - Failed nodes shown as ✕ with dim color
  - Log shows fallback events clearly
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import time
import json
import threading
import math
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────

@dataclass
class NNAPAddress:
    user_id: str
    gps_x: float
    gps_y: float
    gps_z: float
    signal_type: str
    stability: float

    def __str__(self):
        return (f"NA[ID:{self.user_id}, "
                f"GPS:({self.gps_x:.2f},{self.gps_y:.2f},{self.gps_z:.2f}), "
                f"SIG:{self.signal_type}, STB:{self.stability:.2f}]")


@dataclass
class NeuralPacket:
    packet_id: str
    source_address: NNAPAddress
    destination_id: str
    command_code: int
    command_name: str
    signal_quality: float
    emotional_vector: dict
    timestamp: float = field(default_factory=time.time)
    hops: list = field(default_factory=list)
    latency_ms: float = 0.0
    status: str = "PENDING"


@dataclass
class MeshNode:
    node_id: str
    node_type: str
    address: NNAPAddress
    battery: float
    neighbors: list = field(default_factory=list)
    session_state: str = "DISCONNECTED"
    packets_forwarded: int = 0
    is_online: bool = True          # NEW: simulate node failure


# ─────────────────────────────────────────────
#  LAYER 1 – PHYSICAL
# ─────────────────────────────────────────────

class PhysicalLayer:
    SIGNAL_TYPES = ["Alpha", "Beta", "Gamma", "Theta"]

    def generate_neural_signal(self, quality=None):
        quality = quality if quality is not None else random.uniform(0.5, 1.0)
        return {
            "raw_data": "0x" + "".join(random.choices("0123456789ABCDEF", k=8)),
            "signal_quality": round(quality, 3),
            "signal_type": random.choice(self.SIGNAL_TYPES),
            "timestamp": time.time(),
            "source_node": "LOCAL_BCI_HEADSET",
        }

    def transmit_neural_signal(self, packet, brain_node, edge_node):
        # Fail if source node is offline OR stability too low
        if not brain_node.is_online:
            return {"success": False, "latency_ms": None, "reason": "NODE_OFFLINE"}
        success = packet.source_address.stability >= 0.5
        return {
            "success": success,
            "latency_ms": random.uniform(5, 20) if success else None,
            "reason": "OK" if success else "LOW_SIGNAL_STABILITY",
        }

    def receive_at_edge(self, node_address):
        return {
            "buffer_ready": True,
            "node": str(node_address),
            "received_at": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        }


# ─────────────────────────────────────────────
#  LAYER 2 – DATA LINK (NNAP)
# ─────────────────────────────────────────────

class DataLinkLayer:
    def __init__(self):
        self._address_table = {}

    def register_node(self, user_id, address):
        self._address_table[user_id] = address

    def request_resolve(self, target_user_id, priority="HIGH"):
        addr = self._address_table.get(target_user_id)
        if addr:
            return {"status": "SUCCESS", "neuro_address": str(addr),
                    "resolution_time_ms": round(random.uniform(10, 60), 2)}
        return {"status": "NOT_FOUND", "neuro_address": None, "resolution_time_ms": 0}

    def check_link_stability(self, address):
        stable = address.stability >= 0.5
        return {"stable": stable, "stability_value": address.stability,
                "action": "KEEP" if stable else "REROUTE"}


# ─────────────────────────────────────────────
#  LAYER 3 – NETWORK (MDR)
# ─────────────────────────────────────────────

class NetworkLayer:
    ALPHA = 0.5
    BETA  = 0.3
    GAMMA = 0.2

    def calculate_cost(self, noise, distance, battery):
        return round(self.ALPHA*noise + self.BETA*distance + self.GAMMA*(1-battery), 4)

    def find_best_route(self, source, destination_id, all_nodes):
        """Find lowest-cost relay node. Only considers ONLINE nodes with stability >= 0.5."""
        routes = []
        candidates = [n for n in all_nodes
                      if n.node_id != source.node_id
                      and n.node_id != destination_id
                      and n.address.stability >= 0.5
                      and n.is_online
                      and n.node_type == "EDGE"]   # เฉพาะ EDGE เท่านั้นที่เป็น relay ได้

        for node in candidates:
            noise = 1 - node.address.stability
            dist  = math.sqrt((node.address.gps_x - source.address.gps_x)**2 +
                               (node.address.gps_y - source.address.gps_y)**2)
            cost  = self.calculate_cost(noise, min(dist/100, 1.0), node.battery)
            routes.append((cost, node))

        if not routes:
            # Try direct route (no relay)
            return {"success": True, "path": [source.node_id, destination_id],
                    "total_cost": 0.99, "via_node": None, "direct": True}

        routes.sort(key=lambda x: x[0])
        best_cost, best_node = routes[0]
        return {"success": True, "path": [source.node_id, best_node.node_id, destination_id],
                "total_cost": best_cost, "via_node": best_node.node_id, "direct": False}

    def find_fallback_destination(self, original_dest_id, all_nodes):
        """Find backup CLOUD node when primary destination is down."""
        backups = [n for n in all_nodes
                   if n.node_type == "CLOUD"
                   and n.node_id != original_dest_id
                   and n.is_online
                   and n.address.stability >= 0.5]
        if not backups:
            return None
        # Pick highest stability backup
        backups.sort(key=lambda n: n.address.stability, reverse=True)
        return backups[0]


# ─────────────────────────────────────────────
#  LAYER 4 – TRANSPORT (NPI)
# ─────────────────────────────────────────────

class TransportLayer:
    RULES = {
        "R001": ("Unauthorized Access",     "BLOCK_AND_ALERT"),
        "R002": ("Signal Distortion",       "REQUEST_RETRANSMIT"),
        "R003": ("Command Buffer Overflow", "RATE_LIMIT"),
    }

    def verify_packet(self, packet, authorized_ids):
        violations = []
        if packet.source_address.user_id not in authorized_ids:
            violations.append(("R001", *self.RULES["R001"]))
        if packet.signal_quality < 0.4:
            violations.append(("R002", *self.RULES["R002"]))
        if len(packet.hops) > 10:
            violations.append(("R003", *self.RULES["R003"]))
        if violations:
            rule_id, desc, action = violations[0]
            return {"pass": False, "rule": rule_id, "description": desc, "action": action}
        return {"pass": True, "rule": None, "action": "FORWARD"}


# ─────────────────────────────────────────────
#  LAYER 5 – SESSION (BSP)
# ─────────────────────────────────────────────

class SessionLayer:
    STATES = ["DISCONNECTED", "CALIBRATING", "SYNCED", "ACTIVE", "STANDBY", "CLOSED"]

    def __init__(self):
        self._node_states = {}

    def get_state(self, node_id):
        return self.STATES[self._node_states.get(node_id, 0)]

    def advance_state(self, node_id):
        idx = self._node_states.get(node_id, 0)
        if idx < len(self.STATES) - 1:
            idx += 1
        self._node_states[node_id] = idx
        return {"node_id": node_id, "new_state": self.STATES[idx]}

    def reset_state(self, node_id):
        self._node_states[node_id] = 0

    def calibrate(self, node):
        success = node.address.stability >= 0.5
        return {"calibration_ok": success, "stability": node.address.stability,
                "next_state": "SYNCED" if success else "DISCONNECTED"}


# ─────────────────────────────────────────────
#  LAYER 6 – PRESENTATION
# ─────────────────────────────────────────────

class PresentationLayer:
    THOUGHT_MAP = {
        "Move Forward":  0x01,
        "Stop":          0x02,
        "Turn Left":     0x03,
        "Turn Right":    0x04,
        "SOS Emergency": 0x05,
        "Share Vision":  0x06,
        "Send Message":  0x07,
    }

    def encode_thought(self, thought, brain_waves):
        code = self.THOUGHT_MAP.get(thought, 0xFF)
        payload = json.dumps({"command": thought, "code": hex(code),
                               "wave_type": brain_waves.get("signal_type"),
                               "quality": brain_waves.get("signal_quality")})
        return {"encoded": True, "command_code": code,
                "payload_json": payload, "bytes": len(payload)}

    def decode_to_neural_feedback(self, data):
        code = data.get("command_code", 0xFF)
        cmd  = {v: k for k, v in self.THOUGHT_MAP.items()}.get(code, "UNKNOWN")
        return f"[Neural Feedback] Received command '{cmd}' (code={hex(code)})"


# ─────────────────────────────────────────────
#  LAYER 7 – APPLICATION
# ─────────────────────────────────────────────

class ApplicationLayer:
    def thought_to_text(self, thought, sender_id):
        return {"app": "Thought-to-Text Messenger", "message": thought,
                "sender": sender_id, "delivered": True,
                "timestamp": datetime.now().isoformat()}

    def emergency_beacon(self, address):
        return {"app": "Emergency Brain-Beacon", "alert": "SOS",
                "gps": f"({address.gps_x:.4f}, {address.gps_y:.4f})",
                "signal_type": address.signal_type, "dispatched": True}

    def collaborative_mesh_mind(self, sender_id, shared_data, mesh_nodes):
        recipients = [n.node_id for n in mesh_nodes
                      if n.node_id != sender_id and n.is_online]
        return {"app": "Collaborative Mesh Mind", "sender": sender_id,
                "broadcast_to": recipients, "shared": shared_data,
                "nodes_reached": len(recipients)}


# ─────────────────────────────────────────────
#  ORCHESTRATOR
# ─────────────────────────────────────────────

class NeuroEdgeMesh:
    def __init__(self):
        self.physical     = PhysicalLayer()
        self.data_link    = DataLinkLayer()
        self.network      = NetworkLayer()
        self.transport    = TransportLayer()
        self.session      = SessionLayer()
        self.presentation = PresentationLayer()
        self.application  = ApplicationLayer()
        self.nodes   = []
        self.packets = []
        self._setup_default_nodes()

    def _setup_default_nodes(self):
        configs = [
            # id          type    gps_x   gps_y  z   wave    stb   bat
            ("USER_001", "BCI",   13.75, 100.50, 0.0, "Alpha", 0.92, 1.0),
            ("EDGE_001", "EDGE",  13.76, 100.51, 0.0, "Beta",  0.88, 0.85),
            ("EDGE_002", "EDGE",  13.74, 100.49, 0.0, "Gamma", 0.75, 0.70),
            ("EDGE_003", "EDGE",  13.77, 100.52, 0.0, "Alpha", 0.5, 0.60),
            ("CLOUD_01", "CLOUD", 13.80, 100.55, 0.0, "Beta",  0.95, 1.0),
            ("CLOUD_02", "CLOUD", 13.79, 100.53, 0.0, "Gamma", 0.90, 1.0),  # NEW backup
        ]
        for uid, ntype, x, y, z, sig, stb, bat in configs:
            addr = NNAPAddress(uid, x, y, z, sig, stb)
            node = MeshNode(uid, ntype, addr, bat)
            self.nodes.append(node)
            self.data_link.register_node(uid, addr)

    def get_node(self, node_id):
        return next((n for n in self.nodes if n.node_id == node_id), None)

    def toggle_node(self, node_id):
        """Simulate node failure / recovery."""
        node = self.get_node(node_id)
        if node:
            node.is_online = not node.is_online
            return node.is_online
        return None

    def send_neural_packet(self, source_id, destination_id, thought, signal_quality=None):
        log   = []
        start = time.perf_counter()
        fallback_used = False
        actual_dest   = destination_id

        raw = self.physical.generate_neural_signal(signal_quality)
        log.append(("L1 Physical",
                    f"Signal | type={raw['signal_type']} | quality={raw['signal_quality']}"))

        source = self.get_node(source_id)
        dest   = self.get_node(destination_id)
        if not source or not dest:
            return {"success": False, "log": log, "error": "Node not found"}

        # ── Check if source is online ──
        tx = self.physical.transmit_neural_signal(
            NeuralPacket("tmp", source.address, destination_id, 0,
                         thought, raw["signal_quality"], {}),
            source, dest)
        log.append(("L1 Physical",
                    f"Transmit → {destination_id} | success={tx['success']} | {tx['reason']}"))
        if not tx["success"]:
            return {"success": False, "log": log, "error": tx["reason"]}

        # ── Check if destination is online; fallback if not ──
        if not dest.is_online:
            log.append(("L3 Network",
                        f"⚠ {destination_id} is OFFLINE → searching for backup..."))
            backup = self.network.find_fallback_destination(destination_id, self.nodes)
            if not backup:
                return {"success": False, "log": log,
                        "error": f"DESTINATION_DOWN: {destination_id} and no backup available"}
            log.append(("L3 Network",
                        f"✓ Fallback → {backup.node_id} (stability={backup.address.stability})"))
            actual_dest   = backup.node_id
            dest          = backup
            fallback_used = True

        # ── Layer 2 ──
        resolve = self.data_link.request_resolve(actual_dest)
        log.append(("L2 Data Link",
                    f"Resolve {actual_dest} → {resolve['status']} | {resolve['resolution_time_ms']} ms"))
        link = self.data_link.check_link_stability(source.address)
        log.append(("L2 Data Link",
                    f"Link stability={link['stability_value']} | action={link['action']}"))
        if not link["stable"]:
            return {"success": False, "log": log, "error": "LOW_LINK_STABILITY"}

        # ── Layer 3: routing ──
        route = self.network.find_best_route(source, actual_dest, self.nodes)
        log.append(("L3 Network",
                    f"Route: {' → '.join(route['path'])} | cost={route['total_cost']}"
                    + (" [DIRECT]" if route.get("direct") else "")))

        # ── Layer 4 ──
        packet = NeuralPacket(
            packet_id        = f"PKT-{random.randint(1000,9999)}",
            source_address   = source.address,
            destination_id   = actual_dest,
            command_code     = self.presentation.THOUGHT_MAP.get(thought, 0xFF),
            command_name     = thought,
            signal_quality   = raw["signal_quality"],
            emotional_vector = {"valence": round(random.uniform(0.3,0.9),2),
                                "arousal":  round(random.uniform(0.3,0.9),2)},
            hops = route["path"],
        )
        auth_ids = [n.node_id for n in self.nodes]
        verify   = self.transport.verify_packet(packet, auth_ids)
        log.append(("L4 Transport",
                    f"Verify → pass={verify['pass']} | action={verify['action']}"))
        if not verify["pass"]:
            return {"success": False, "log": log,
                    "error": f"{verify['rule']}: {verify['description']}"}

        # ── Layer 5 ──
        state = self.session.advance_state(source_id)
        log.append(("L5 Session", f"State → {state['new_state']}"))

        # ── Layer 6 ──
        enc = self.presentation.encode_thought(thought, raw)
        log.append(("L6 Presentation",
                    f"Encode '{thought}' → code={hex(enc['command_code'])} | {enc['bytes']} bytes"))

        # ── Layer 7 ──
        if thought == "SOS Emergency":
            app = self.application.emergency_beacon(source.address)
        elif thought == "Share Vision":
            app = self.application.collaborative_mesh_mind(source_id, thought, self.nodes)
        else:
            app = self.application.thought_to_text(thought, source_id)
        log.append(("L7 Application",
                    f"App={app['app']} | result="
                    f"{app.get('delivered', app.get('dispatched', app.get('nodes_reached','?')))}"))

        elapsed           = (time.perf_counter() - start) * 1000
        packet.latency_ms = round(elapsed + random.uniform(10, 40), 2)
        packet.status     = "DELIVERED"
        self.packets.append(packet)
        source.packets_forwarded += 1

        return {
            "success":          True,
            "log":              log,
            "packet":           packet,
            "app_result":       app,
            "total_latency_ms": packet.latency_ms,
            "fallback_used":    fallback_used,
            "original_dest":    destination_id,
            "actual_dest":      actual_dest,
        }


# ─────────────────────────────────────────────
#  COLORS & CONSTANTS
# ─────────────────────────────────────────────

COLORS = {
    "bg":       "#0A0E1A",
    "panel":    "#111827",
    "border":   "#1E3A5F",
    "accent1":  "#00D4FF",
    "accent2":  "#7C3AED",
    "accent3":  "#10B981",
    "warn":     "#F59E0B",
    "danger":   "#EF4444",
    "offline":  "#374151",
    "text":     "#E2E8F0",
    "subtext":  "#94A3B8",
    "layer_bg": "#0D1B2A",
}

LAYER_COLORS = {
    "L1 Physical":     "#EF4444",
    "L2 Data Link":    "#F59E0B",
    "L3 Network":      "#10B981",
    "L4 Transport":    "#3B82F6",
    "L5 Session":      "#8B5CF6",
    "L6 Presentation": "#EC4899",
    "L7 Application":  "#00D4FF",
}

NODE_TYPE_COLOR = {
    "BCI":   "#00D4FF",
    "EDGE":  "#10B981",
    "CLOUD": "#7C3AED",
}

# Canvas positions – hexagon layout for 6 nodes
NODE_POSITIONS = {
    "USER_001": ( 90, 220),   # left
    "EDGE_001": (230,  65),   # top-left
    "EDGE_002": (230, 375),   # bottom-left
    "EDGE_003": (390,  65),   # top-right
    "CLOUD_01": (460, 150),   # right-top   (primary)
    "CLOUD_02": (460, 290),   # right-bottom (backup)
}

NODE_RADIUS = 28


# ─────────────────────────────────────────────
#  MESH TOPOLOGY CANVAS
# ─────────────────────────────────────────────

class MeshTopologyCanvas(tk.Frame):
    def __init__(self, parent, mesh: NeuroEdgeMesh, on_node_toggle=None, **kwargs):
        super().__init__(parent, bg=COLORS["panel"], **kwargs)
        self.mesh            = mesh
        self.on_node_toggle  = on_node_toggle   # callback when user clicks a node

        hdr = tk.Frame(self, bg=COLORS["panel"])
        hdr.pack(fill="x", padx=8, pady=(6, 2))
        tk.Label(hdr, text="⬡ MESH TOPOLOGY  (MDR)",
                 bg=COLORS["panel"], fg=COLORS["accent1"],
                 font=("Courier New", 10, "bold")).pack(side="left")
        tk.Label(hdr, text="  [click node to toggle ON/OFF]",
                 bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 8)).pack(side="left")
        tk.Frame(self, bg=COLORS["accent1"], height=1).pack(fill="x", padx=8)

        self.canvas = tk.Canvas(self, bg=COLORS["layer_bg"],
                                 highlightthickness=0, width=560, height=450)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=6)

        # Legend
        leg = tk.Frame(self, bg=COLORS["panel"])
        leg.pack(fill="x", padx=8, pady=(0, 4))
        for label, color in [("BCI", NODE_TYPE_COLOR["BCI"]),
                              ("EDGE", NODE_TYPE_COLOR["EDGE"]),
                              ("CLOUD (primary)", NODE_TYPE_COLOR["CLOUD"]),
                              ("CLOUD (backup)", "#A78BFA"),
                              ("Active Route", COLORS["warn"]),
                              ("Weak/Offline", COLORS["danger"])]:
            tk.Label(leg, text="●", bg=COLORS["panel"], fg=color,
                     font=("Courier New", 11)).pack(side="left", padx=(6,1))
            tk.Label(leg, text=label, bg=COLORS["panel"], fg=COLORS["subtext"],
                     font=("Courier New", 8)).pack(side="left", padx=(0,8))

        self._active_edges: list = []
        self._anim_job           = None
        self._edge_items: dict   = {}
        self._node_items: dict   = {}

        self._draw_base()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    # ── Drawing ────────────────────────────────────────────────

    def _draw_base(self):
        self.canvas.delete("all")
        self._edge_items = {}
        self._node_items = {}

        # Background grid dots
        for x in range(0, 580, 30):
            for y in range(0, 470, 30):
                self.canvas.create_oval(x, y, x+1, y+1,
                                         fill="#1E3A5F", outline="")

        nodes = self.mesh.nodes
        for i, na in enumerate(nodes):
            for nb in nodes[i+1:]:
                self._draw_edge(na, nb)
        for node in nodes:
            self._draw_node(node)

    def _edge_color(self, na, nb):
        if not na.is_online or not nb.is_online:
            return COLORS["offline"], (6, 4)
        if na.address.stability < 0.5 or nb.address.stability < 0.5:
            return COLORS["danger"], (4, 4)
        return COLORS["border"], ()

    def _draw_edge(self, na, nb):
        if na.node_id not in NODE_POSITIONS or nb.node_id not in NODE_POSITIONS:
            return
        ax, ay = NODE_POSITIONS[na.node_id]
        bx, by = NODE_POSITIONS[nb.node_id]

        noise = 1 - min(na.address.stability, nb.address.stability)
        dist  = math.sqrt((ax-bx)**2 + (ay-by)**2)
        cost  = round(0.5*noise + 0.3*min(dist/200,1.0) + 0.2*(1-min(na.battery,nb.battery)), 2)

        color, dash = self._edge_color(na, nb)
        lid = self.canvas.create_line(ax, ay, bx, by,
                                       fill=color, width=1.5,
                                       dash=dash, tags="edge")
        key = tuple(sorted([na.node_id, nb.node_id]))
        self._edge_items[key] = lid

        if na.is_online and nb.is_online:
            mx, my = (ax+bx)//2, (ay+by)//2
            self.canvas.create_rectangle(mx-14, my-9, mx+14, my+2,
                                          fill=COLORS["layer_bg"], outline="")
            self.canvas.create_text(mx, my-4, text=f"{cost}",
                                     fill="#4B6A88",
                                     font=("Courier New", 8, "bold"),
                                     tags="cost_label")

    def _node_color(self, node):
        if not node.is_online:
            return COLORS["offline"]
        if node.address.stability < 0.5:
            return COLORS["danger"]
        # CLOUD_02 gets a lighter purple to distinguish from CLOUD_01
        if node.node_id == "CLOUD_02":
            return "#A78BFA"
        return NODE_TYPE_COLOR.get(node.node_type, COLORS["accent1"])

    def _draw_node(self, node):
        if node.node_id not in NODE_POSITIONS:
            return
        cx, cy = NODE_POSITIONS[node.node_id]
        r      = NODE_RADIUS
        color  = self._node_color(node)

        # Glow rings (skip if offline)
        if node.is_online:
            self.canvas.create_oval(cx-r-6, cy-r-6, cx+r+6, cy+r+6,
                                      outline=color, fill="", width=1,
                                      stipple="gray12", tags="glow")
            self.canvas.create_oval(cx-r-2, cy-r-2, cx+r+2, cy+r+2,
                                      outline=color, fill="", width=1,
                                      stipple="gray50", tags="glow")

        # Main circle
        cid = self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                       fill=COLORS["layer_bg"],
                                       outline=color, width=2,
                                       tags=("node", node.node_id))
        self._node_items[node.node_id] = cid

        # Label inside
        short = (node.node_id
                 .replace("USER_0","U").replace("EDGE_0","E").replace("CLOUD_0","C"))
        label = short if node.is_online else "✕"
        self.canvas.create_text(cx, cy, text=label,
                                 fill=color, font=("Courier New", 9, "bold"),
                                 tags=("node_label", node.node_id))

        # Full ID & type below
        self.canvas.create_text(cx, cy+r+12, text=node.node_id,
                                  fill=COLORS["subtext"] if node.is_online else COLORS["offline"],
                                  font=("Courier New", 7), tags="node_fullid")
        type_str = f"[{node.node_type}]" + ("" if node.is_online else " OFFLINE")
        self.canvas.create_text(cx, cy+r+23,
                                  text=type_str,
                                  fill=self._node_color(node),
                                  font=("Courier New", 7), tags="node_type")

        # Stability above
        stb_color = COLORS["offline"] if not node.is_online else \
                    (COLORS["danger"] if node.address.stability < 0.5 else COLORS["accent3"])
        self.canvas.create_text(cx, cy-r-14,
                                  text=f"{node.address.stability:.2f}",
                                  fill=stb_color,
                                  font=("Courier New", 9, "bold"),
                                  tags="node_stb")

        # "BACKUP" badge for CLOUD_02
        if node.node_id == "CLOUD_02":
            self.canvas.create_text(cx, cy-r-26, text="BACKUP",
                                     fill="#A78BFA",
                                     font=("Courier New", 7, "bold"),
                                     tags="backup_badge")

    # ── Interaction ────────────────────────────────────────────

    def _on_canvas_click(self, event):
        """Toggle node online/offline when user clicks on it."""
        for node in self.mesh.nodes:
            if node.node_id not in NODE_POSITIONS:
                continue
            cx, cy = NODE_POSITIONS[node.node_id]
            if math.sqrt((event.x - cx)**2 + (event.y - cy)**2) <= NODE_RADIUS + 6:
                self.mesh.toggle_node(node.node_id)
                self.refresh()
                if self.on_node_toggle:
                    self.on_node_toggle(node.node_id, node.is_online)
                return

    # ── Public API ─────────────────────────────────────────────

    def refresh(self):
        if self._anim_job:
            self.canvas.after_cancel(self._anim_job)
            self._anim_job = None
        self._draw_base()

    def animate_route(self, path, success, fallback=False, on_done=None):
        self._clear_highlights()
        valid_path = [p for p in path if p in NODE_POSITIONS]
        if len(valid_path) < 2:
            return

        route_color = "#FF9F1C" if fallback else (COLORS["warn"] if success else COLORS["danger"])

        for i in range(len(valid_path) - 1):
            key = tuple(sorted([valid_path[i], valid_path[i+1]]))
            eid = self._edge_items.get(key)
            if eid:
                self.canvas.itemconfig(eid, fill=route_color, width=3, dash=())
                self._active_edges.append(eid)

        src_id = self._node_items.get(valid_path[0])
        if src_id:
            self.canvas.itemconfig(src_id, outline=COLORS["warn"], width=3)

        waypoints = [NODE_POSITIONS[n] for n in valid_path]
        dot_color = COLORS["accent3"] if success else COLORS["danger"]
        if fallback:
            dot_color = "#FF9F1C"

        self.canvas.create_oval(0,0,0,0, fill=dot_color, outline="white",
                                 width=1.5, tags="packet_dot")
        self.canvas.create_oval(0,0,0,0, fill="", outline=dot_color,
                                 width=1, stipple="gray50", tags="packet_trail")
        self._animate_dot(waypoints, 0, 0.0, dot_color, on_done)

    def _animate_dot(self, waypoints, seg, t, color, on_done):
        if seg >= len(waypoints) - 1:
            self.canvas.delete("packet_dot")
            self.canvas.delete("packet_trail")
            self._anim_job = self.canvas.after(700, self._clear_highlights)
            if on_done:
                on_done()
            return

        ax, ay = waypoints[seg]
        bx, by = waypoints[seg + 1]
        steps  = 35
        if t >= 1.0:
            self._animate_dot(waypoints, seg+1, 0.0, color, on_done)
            return

        ease = t * t * (3 - 2*t)
        cx   = ax + (bx-ax) * ease
        cy   = ay + (by-ay) * ease
        r    = 7 + 2 * math.sin(t * math.pi)
        tr   = r + 5
        self.canvas.coords("packet_dot",   cx-r,  cy-r,  cx+r,  cy+r)
        self.canvas.coords("packet_trail", cx-tr, cy-tr, cx+tr, cy+tr)
        self._anim_job = self.canvas.after(
            18, self._animate_dot, waypoints, seg, t + 1.0/steps, color, on_done)

    def _clear_highlights(self):
        for eid in self._active_edges:
            try:
                self.canvas.itemconfig(eid, fill=COLORS["border"], width=1.5, dash=())
            except tk.TclError:
                pass
        self._active_edges.clear()
        self.canvas.delete("packet_dot")
        self.canvas.delete("packet_trail")
        for node in self.mesh.nodes:
            nid = self._node_items.get(node.node_id)
            if nid:
                try:
                    self.canvas.itemconfig(nid, outline=self._node_color(node), width=2)
                except tk.TclError:
                    pass

    def highlight_node(self, node_id, color):
        nid = self._node_items.get(node_id)
        if nid:
            self.canvas.itemconfig(nid, outline=color, width=3)


# ─────────────────────────────────────────────
#  MAIN GUI
# ─────────────────────────────────────────────

class NeuroEdgeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.mesh = NeuroEdgeMesh()
        self.root.title("NeuroEdge Mesh Network Simulator v1.2")
        self.root.configure(bg=COLORS["bg"])
        self.root.geometry("1540x900")
        self.root.resizable(True, True)
        self._build_ui()
        self._update_node_table()

    # ── UI ─────────────────────────────────────────────────────

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=COLORS["bg"], pady=8)
        hdr.pack(fill="x", padx=16)
        tk.Label(hdr, text="⬡ NEUROEDGE MESH NETWORK SIMULATOR",
                 bg=COLORS["bg"], fg=COLORS["accent1"],
                 font=("Courier New", 15, "bold")).pack(side="left")
        tk.Label(hdr, text="CP352005 Networks  •  v1.2  •  CLOUD Redundancy Edition",
                 bg=COLORS["bg"], fg=COLORS["subtext"],
                 font=("Courier New", 9)).pack(side="right")

        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=12, pady=4)

        col_left   = tk.Frame(main, bg=COLORS["bg"], width=450)
        col_center = tk.Frame(main, bg=COLORS["bg"], width=580)
        col_right  = tk.Frame(main, bg=COLORS["bg"])

        col_left.pack(side="left", fill="y", padx=(0,5))
        col_left.pack_propagate(False)
        col_center.pack(side="left", fill="y", padx=5)
        col_center.pack_propagate(False)
        col_right.pack(side="right", fill="both", expand=True, padx=(5,0))

        self._build_control_panel(col_left)
        self._build_node_panel(col_left)
        self._build_topology_panel(col_center)
        self._build_layer_log(col_right)
        self._build_stats_bar()

    def _panel(self, parent, title, color=None):
        c = color or COLORS["accent1"]
        f = tk.Frame(parent, bg=COLORS["panel"],
                     highlightbackground=c, highlightthickness=1)
        f.pack(fill="both", expand=True, pady=4)
        tk.Label(f, text=f" {title}", bg=COLORS["panel"], fg=c,
                 font=("Courier New", 10, "bold"), anchor="w").pack(
            fill="x", padx=8, pady=(6,2))
        tk.Frame(f, bg=c, height=1).pack(fill="x", padx=8)
        return f

    def _btn(self, parent, text, cmd, color, **kw):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="white",
                         font=("Courier New", 9, "bold"),
                         relief="flat", cursor="hand2",
                         padx=10, pady=5, bd=0,
                         activebackground=color, activeforeground="white", **kw)

    def _build_control_panel(self, parent):
        panel = self._panel(parent, "◉ TRANSMISSION CONTROL", COLORS["accent1"])

        r1 = tk.Frame(panel, bg=COLORS["panel"])
        r1.pack(fill="x", padx=10, pady=6)
        node_ids = [n.node_id for n in self.mesh.nodes]

        tk.Label(r1, text="SOURCE:", bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 9)).grid(row=0, column=0, sticky="w", padx=4)
        self.var_source = tk.StringVar(value="USER_001")
        ttk.Combobox(r1, textvariable=self.var_source, values=node_ids,
                     width=11, state="readonly").grid(row=0, column=1, padx=4)

        tk.Label(r1, text="DEST:", bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 9)).grid(row=0, column=2, sticky="w", padx=4)
        self.var_dest = tk.StringVar(value="CLOUD_01")
        ttk.Combobox(r1, textvariable=self.var_dest, values=node_ids,
                     width=11, state="readonly").grid(row=0, column=3, padx=4)

        r2 = tk.Frame(panel, bg=COLORS["panel"])
        r2.pack(fill="x", padx=10, pady=4)
        tk.Label(r2, text="COMMAND:", bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 9)).grid(row=0, column=0, sticky="w", padx=4)
        self.var_thought = tk.StringVar(value="Move Forward")
        ttk.Combobox(r2, textvariable=self.var_thought,
                     values=list(PresentationLayer.THOUGHT_MAP.keys()),
                     width=14, state="readonly").grid(row=0, column=1, padx=4)

        tk.Label(r2, text="QUALITY:", bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 9)).grid(row=0, column=2, sticky="w", padx=4)
        self.var_quality = tk.DoubleVar(value=0.85)
        tk.Scale(r2, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
                 variable=self.var_quality, bg=COLORS["panel"], fg=COLORS["accent1"],
                 troughcolor=COLORS["border"], highlightthickness=0,
                 length=100).grid(row=0, column=3, padx=4)

        bf = tk.Frame(panel, bg=COLORS["panel"])
        bf.pack(fill="x", padx=10, pady=(4,8))
        self._btn(bf, "▶  TRANSMIT",   self._transmit,       COLORS["accent3"]).pack(side="left",  padx=3)
        self._btn(bf, "↺  AUTO DEMO",  self._start_demo,     COLORS["accent2"]).pack(side="left",  padx=3)
        self._btn(bf, "⬡  SESSION+",   self._advance_session, COLORS["warn"]).pack(side="left",    padx=3)
        self._btn(bf, "✕  CLEAR",      self._clear_log,      COLORS["danger"]).pack(side="right",  padx=3)

    def _build_node_panel(self, parent):
        panel = self._panel(parent, "⬡ MESH NODES  (click topology to toggle)", COLORS["accent2"])
        cols  = ("ID", "Type", "Wave", "Stab", "Bat", "Status", "Pkts")
        self.node_tree = ttk.Treeview(panel, columns=cols, show="headings", height=8)
        for col, w in zip(cols, [82, 52, 52, 48, 45, 80, 35]):
            self.node_tree.heading(col, text=col)
            self.node_tree.column(col, width=w, anchor="center")

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=COLORS["layer_bg"],
                    foreground=COLORS["text"], fieldbackground=COLORS["layer_bg"],
                    font=("Courier New", 8), rowheight=20)
        s.configure("Treeview.Heading", background=COLORS["border"],
                    foreground=COLORS["accent2"], font=("Courier New", 8, "bold"))
        self.node_tree.pack(fill="both", expand=True, padx=8, pady=6)

    def _build_topology_panel(self, parent):
        outer = tk.Frame(parent, bg=COLORS["panel"],
                         highlightbackground=COLORS["warn"], highlightthickness=1)
        outer.pack(fill="both", expand=True, pady=4)

        self.topology = MeshTopologyCanvas(outer, self.mesh,
                                            on_node_toggle=self._on_node_toggled)
        self.topology.pack(fill="both", expand=True)

        bf = tk.Frame(outer, bg=COLORS["panel"])
        bf.pack(fill="x", padx=8, pady=(0,8))
        self._btn(bf, "▶  RUN SIM",    self._transmit,      COLORS["accent3"]).pack(side="left", padx=4)
        self._btn(bf, "⚡  EMERGENCY", self._emergency,      COLORS["danger"]).pack(side="left",  padx=4)
        self._btn(bf, "↺  RESET",     self._reset_topology, COLORS["subtext"]).pack(side="left", padx=4)

        # Hint label
        tk.Label(outer, text="💡 คลิกโหนดบน canvas เพื่อทำให้ล้ม / ฟื้นตัว",
                 bg=COLORS["panel"], fg=COLORS["subtext"],
                 font=("Courier New", 8)).pack(pady=(0,4))

    def _build_layer_log(self, parent):
        panel = self._panel(parent, "◈ 7-LAYER TRANSMISSION LOG", COLORS["accent3"])
        self.log_text = scrolledtext.ScrolledText(
            panel, bg=COLORS["layer_bg"], fg=COLORS["text"],
            font=("Courier New", 9), relief="flat",
            insertbackground=COLORS["accent1"], wrap="word",
            state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=8, pady=6)
        for layer, color in LAYER_COLORS.items():
            self.log_text.tag_configure(layer, foreground=color)
        self.log_text.tag_configure("header",   foreground=COLORS["accent1"],
                                    font=("Courier New", 9, "bold"))
        self.log_text.tag_configure("success",  foreground=COLORS["accent3"])
        self.log_text.tag_configure("fallback", foreground="#FF9F1C",
                                    font=("Courier New", 9, "bold"))
        self.log_text.tag_configure("error",    foreground=COLORS["danger"])
        self.log_text.tag_configure("info",     foreground=COLORS["subtext"])
        self.log_text.tag_configure("toggle",   foreground=COLORS["warn"],
                                    font=("Courier New", 9, "bold"))

    def _build_stats_bar(self):
        bar = tk.Frame(self.root, bg=COLORS["panel"], height=28)
        bar.pack(fill="x", side="bottom")
        self.lbl_packets = tk.Label(bar, text="PACKETS: 0",
                                    bg=COLORS["panel"], fg=COLORS["accent1"],
                                    font=("Courier New", 9, "bold"))
        self.lbl_packets.pack(side="left", padx=12)
        self.lbl_latency = tk.Label(bar, text="AVG LATENCY: — ms",
                                    bg=COLORS["panel"], fg=COLORS["accent3"],
                                    font=("Courier New", 9, "bold"))
        self.lbl_latency.pack(side="left", padx=12)
        self.lbl_fallback = tk.Label(bar, text="FALLBACKS: 0",
                                     bg=COLORS["panel"], fg="#FF9F1C",
                                     font=("Courier New", 9, "bold"))
        self.lbl_fallback.pack(side="left", padx=12)
        self.lbl_status = tk.Label(bar, text="STATUS: IDLE",
                                   bg=COLORS["panel"], fg=COLORS["warn"],
                                   font=("Courier New", 9, "bold"))
        self.lbl_status.pack(side="right", padx=12)
        self._fallback_count = 0

    # ── Actions ────────────────────────────────────────────────

    def _transmit(self):
        src     = self.var_source.get()
        dst     = self.var_dest.get()
        thought = self.var_thought.get()
        quality = self.var_quality.get()

        if src == dst:
            messagebox.showwarning("Invalid", "Source and destination must differ.")
            return

        self.lbl_status.config(text="STATUS: TRANSMITTING…", fg=COLORS["warn"])
        self.root.update()

        result = self.mesh.send_neural_packet(src, dst, thought, quality)
        self._render_log(src, dst, thought, result)
        self._update_node_table()
        self._update_stats(result)

        hops = result["packet"].hops if result["success"] else [src, dst]
        self.topology.animate_route(hops, result["success"],
                                    fallback=result.get("fallback_used", False))

    def _emergency(self):
        self.var_source.set("USER_001")
        self.var_dest.set("CLOUD_01")
        self.var_thought.set("SOS Emergency")
        self.var_quality.set(0.9)
        self._transmit()

    def _reset_topology(self):
        # Bring all nodes back online first
        for node in self.mesh.nodes:
            node.is_online = True
        self.topology.refresh()
        self._update_node_table()
        self._append_log("[Reset] All nodes restored to ONLINE", "toggle")

    def _on_node_toggled(self, node_id, is_online):
        status = "ONLINE ✓" if is_online else "OFFLINE ✕"
        color  = "success" if is_online else "error"
        self._append_log(f"[Node Toggle] {node_id} → {status}", color)
        self._update_node_table()

    def _render_log(self, src, dst, thought, result):
        self.log_text.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.insert("end", f"\n{'─'*58}\n", "info")

        # Show fallback warning in header if used
        if result.get("fallback_used"):
            orig = result.get("original_dest", dst)
            actual = result.get("actual_dest", dst)
            self.log_text.insert("end",
                f"[{ts}] {src} → {orig}  |  '{thought}'\n", "header")
            self.log_text.insert("end",
                f"  ⚡ FALLBACK ACTIVATED: {orig} is DOWN → rerouted to {actual}\n", "fallback")
        else:
            self.log_text.insert("end",
                f"[{ts}] {src} → {dst}  |  '{thought}'\n", "header")

        for layer, msg in result.get("log", []):
            tag = layer if layer in LAYER_COLORS else "info"
            self.log_text.insert("end", f"  [{layer}]  ", tag)
            self.log_text.insert("end", f"{msg}\n")

        if result["success"]:
            pkt = result["packet"]
            suffix = f"  ⚡ via BACKUP {result['actual_dest']}" if result.get("fallback_used") else ""
            self.log_text.insert("end",
                f"\n  ✓ DELIVERED  |  {result['total_latency_ms']} ms"
                f"  |  {' → '.join(pkt.hops)}{suffix}\n",
                "fallback" if result.get("fallback_used") else "success")
        else:
            self.log_text.insert("end",
                f"\n  ✗ FAILED  |  {result.get('error','Unknown')}\n", "error")

        self.log_text.config(state="disabled")
        self.log_text.see("end")

        ok = result["success"]
        fb = result.get("fallback_used", False)
        self.lbl_status.config(
            text="STATUS: FALLBACK DELIVERED" if (ok and fb) else
                 ("STATUS: DELIVERED" if ok else "STATUS: FAILED"),
            fg="#FF9F1C" if (ok and fb) else
               (COLORS["accent3"] if ok else COLORS["danger"]))

    def _advance_session(self):
        nid = self.var_source.get()
        res = self.mesh.session.advance_state(nid)
        self._append_log(f"[Session] {nid} → {res['new_state']}", "info")
        self._update_node_table()

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def _append_log(self, text, tag="info"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n", tag)
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def _start_demo(self):
        def _run():
            thoughts = list(PresentationLayer.THOUGHT_MAP.keys())
            node_ids = [n.node_id for n in self.mesh.nodes]
            for _ in range(6):
                src  = random.choice([n for n in node_ids if "USER" in n or "BCI" in n] or node_ids)
                dst  = random.choice([n for n in node_ids if n != src])
                cmd  = random.choice(thoughts)
                qual = round(random.uniform(0.5, 1.0), 2)
                result = self.mesh.send_neural_packet(src, dst, cmd, qual)
                hops   = result["packet"].hops if result["success"] else [src, dst]
                self.root.after(0, self._render_log, src, dst, cmd, result)
                self.root.after(0, self._update_node_table)
                self.root.after(0, self._update_stats, result)
                self.root.after(0, self.topology.animate_route, hops,
                                result["success"], result.get("fallback_used", False))
                time.sleep(1.4)
        threading.Thread(target=_run, daemon=True).start()

    # ── Helpers ────────────────────────────────────────────────

    def _update_node_table(self):
        for row in self.node_tree.get_children():
            self.node_tree.delete(row)
        for node in self.mesh.nodes:
            state  = self.mesh.session.get_state(node.node_id)
            stb    = node.address.stability
            online = "ONLINE" if node.is_online else "OFFLINE"
            tag    = "offline" if not node.is_online else ("weak" if stb < 0.5 else "")
            # Mark CLOUD_02 as backup
            display_type = node.node_type + ("*" if node.node_id == "CLOUD_02" else "")
            self.node_tree.insert("", "end", values=(
                node.node_id, display_type, node.address.signal_type,
                f"{stb:.2f}", f"{node.battery:.0%}",
                online, node.packets_forwarded,
            ), tags=(tag,))
        self.node_tree.tag_configure("weak",    foreground=COLORS["danger"])
        self.node_tree.tag_configure("offline", foreground=COLORS["offline"])

    def _update_stats(self, result=None):
        total = len(self.mesh.packets)
        self.lbl_packets.config(text=f"PACKETS: {total}")
        if self.mesh.packets:
            avg = sum(p.latency_ms for p in self.mesh.packets) / total
            self.lbl_latency.config(text=f"AVG LATENCY: {avg:.1f} ms")
        if result and result.get("fallback_used"):
            self._fallback_count += 1
            self.lbl_fallback.config(text=f"FALLBACKS: {self._fallback_count}")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    root = tk.Tk()
    NeuroEdgeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()