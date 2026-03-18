# 💻 NeuroEdge Mesh Network
## 4. IMPLEMENTATION — Core Development Deep Dive

> **Course:** CP352005 Networks | **Sprint-01:** "First Whisper" | **Team:** NeuroEdge

---

## 4.1 Implementation Priorities (MoSCoW)

### ลำดับความสำคัญ 1 — Must Have (ต้องมี)
- คลาส `NeuroNodeAddress` (ที่อยู่ 24-byte)
- ระบบจัดการตารางเส้นทาง (Routing Table Manager)
- Modified Dijkstra Algorithm ถ่วงน้ำหนักด้วย SNR
- โครงสร้าง Thought Packet + ระบบจำลองเบื้องต้น

### ลำดับความสำคัญ 2 — Should Have (ควรมี)
- ระบบ Cache เส้นทางเพื่อลด Latency
- Visualization ของเครือข่าย Mesh
- การเพิ่มประสิทธิภาพการประมวลผลบนชิปจำลอง

### ลำดับความสำคัญ 3 — Nice to Have (ถ้ามีจะดีมาก)
- GUI สำหรับตรวจสอบสถานะโหนด
- Real-time Network Status Update

---

## 4.2 Week-by-Week Implementation Roadmap

### Week 1 — Foundation Sprint (Days 1–5)
**Theme:** Architecture, Setup & Component Design

| Day | Focus | Owner | Output |
|---|---|---|---|
| Day 1 (Mon) | Kickoff & Environment Setup | All | GitHub Repo, Dev Environment |
| Day 2 (Tue) | NNAP Address Design | ปิยพันธ์ | NNAP Spec v1.0 (24-byte format) |
| Day 3 (Wed) | MDR Pseudo-code Draft | วรปรัชญ์ | MDR Algorithm Draft |
| Day 4 (Thu) | NPI Rule Engine Design | เนติภัทร | NPI Firewall Rulebook |
| Day 5 (Fri) | Week 1 Sync & Interface Review | All | Architecture Blueprint อนุมัติ |

**Week 1 Success Criteria:**
- [ ] All specifications documented
- [ ] Development environment working for all members
- [ ] Basic simulation framework created
- [ ] Test framework established
- [ ] CI passing on main branch

---

### Week 2 — Implementation Sprint (Days 6–10)
**Theme:** Core Protocol Implementation

| Day | Focus | Owner | Output |
|---|---|---|---|
| Day 6 (Mon) | NNAP Coding (NeuroNodeAddress class) | ปิยพันธ์ | NNAP Module |
| Day 7 (Tue) | BCI Link Simulation (Alpha/Beta noise metrics) | วรปรัชญ์ | BCI Simulation Script |
| Day 8 (Wed) | MDR Logic (Modified Dijkstra + Noise weight) | วรปรัชญ์ | MDR Routing Engine |
| Day 9 (Thu) | Security Engine (Bio-Signature Validation) | เนติภัทร | Bio-Signature Engine |
| Day 10 (Fri) | Mid-Sprint Demo | All | Unit Test Results > 80% coverage |

**Day 6–7 Detail — NNAP Implementation:**
1. Implement `NeuroNodeAddress` class (24-byte format)
2. Create address resolution module (Map Brain ID → Mesh IP)
3. Build BCI link simulation with Alpha/Beta wave noise metrics
4. Write unit tests (minimum 80% coverage)

**Day 8–9 Detail — MDR Implementation (Critical Path):**
1. Implement dynamic routing table management
2. Code Modified Dijkstra with Neuro-metrics (Latency + Noise)
3. Create route calculation module for Mesh Edge Nodes
4. Add route caching mechanism for frequently communicated nodes

> **Critical Path Item:** MDR must be completed by Day 9 EOD

**Day 10 Detail — NPI Security Implementation:**
1. Implement Bio-Signature rule engine
2. Create packet validation pipeline (Drop malicious Thought Packets)
3. Add security violation logging
4. Test with unauthorized access scenarios

**Week 2 Success Criteria:**
- [ ] Address creation and validation working
- [ ] Resolution returns correct physical addresses
- [ ] Link simulation calculates Signal Noise accurately
- [ ] MDR routes packets correctly
- [ ] Route caching reduces recalculation time
- [ ] NPI blocks unauthorized access
- [ ] All unit tests passing

---

### Week 3 — Integration Sprint (Days 11–15)
**Theme:** Pipeline Integration & System Testing

| Day | Focus | Owner | Output |
|---|---|---|---|
| Day 11 (Mon) | Virtual Mesh Network (Node A, B, C) | DevOps | Virtual Mesh Network running |
| Day 12 (Tue) | NNAP + MDR Integration | ปิยพันธ์ + วรปรัชญ์ | Address-Route Pipeline |
| Day 13 (Wed) | Full Stack Sync (NPI คั่นกลาง) | All | Integrated E2E System |
| Day 14 (Thu) | E2E Testing (ส่ง Thought Packet) | Tester | E2E Transmission Log |
| Day 15 (Fri) | Latency Audit & Profiling | All | Performance Audit Report |

**Integration Steps:**
1. สร้างโหนด Mesh จำลอง A, B, C และเส้นทางเชื่อมต่อ
2. เชื่อมต่อระบบระบุที่อยู่ (NNAP) เข้ากับระบบเลือกเส้นทาง (MDR)
3. นำ NPI Security มาวางคั่นกลางระหว่างการส่งข้อมูล
4. ทดสอบส่ง Thought Packet จากต้นทางถึงปลายทาง (E2E)
5. วัดความหน่วงและเก็บข้อมูลประสิทธิภาพ

**Integration Test Scenarios (15+ cases):**
- ส่งแพ็กเก็ตจาก Layer 4 (NPI) ลงไปจนถึง Layer 1 (Physical)
- เลือกเส้นทางใหม่เมื่อโหนด Mesh บางจุดหายไป
- ทดสอบการป้องกัน Thought Injection
- ทดสอบ Self-Healing เมื่อโหนดกลับมา Online

---

### Week 4 — Delivery Sprint (Days 16–20)
**Theme:** Finalization, Optimization & Presentation

| Day | Focus | Owner | Output |
|---|---|---|---|
| Day 16 (Mon) | Stress Test (Node Failure Simulation) | Tester | Self-Healing Report |
| Day 17 (Tue) | Latency Tuning (ตัด Processing ซ้ำซ้อน) | Tech Team | Optimized Build < 50ms |
| Day 18 (Wed) | Bug Bash — 0 Critical Bugs | All | Stable Final Build |
| Day 19 (Thu) | Demo Video + Presentation Prep | All | Slide Deck + Demo Video |
| Day 20 (Fri) | Sprint Review & Retrospective | All | Project Delivery (ZIP + Report) |

**Day 17 Optimization Focus:**
- Code cleanup and comments (PEP 8 for Python)
- Latency optimization (Reduce processing time at Edge Node)
- Edge case handling: What if BCI signal drops completely?
- Visualization UI enhancement

---

## 4.3 Technical Debt Register

| Debt Item | Impact | Mitigation Strategy |
|---|---|---|
| **Routing Algorithm Complexity** | HIGH | ใช้ Dijkstra พื้นฐานแทน AI Routing ในเฟสแรก |
| **Simulation Realism** | MEDIUM | จำลองสัญญาณสมองเป็นตัวเลข ไม่ใช่ BCI จริง |
| **Neural Noise Handling** | MEDIUM | ใช้ Static Filter แทน Dynamic Adaptive Noise Cancellation |
| **Documentation Gaps** | LOW | Document as you code — Comment + README update ทุก Merge |

---

## 4.4 Core Code Structures

### NeuroNodeAddress Class (24-byte)
```python
class NeuroNodeAddress:
    def __init__(self, user_id: str, gps: tuple, signal_type: str, stability: float):
        self.user_id = user_id          # 8 bytes: Unique Brain Signature
        self.gps = gps                  # 8 bytes: (X, Y, Z) coordinates
        self.signal_type = signal_type  # 4 bytes: ALPHA / BETA / GAMMA
        self.stability = stability      # 4 bytes: Link Stability (0.0-1.0)

    def is_valid(self) -> bool:
        """โหนดถูกต้องเมื่อ stability > 0.5"""
        return self.stability > 0.5

    def resolve_to_mesh_ip(self) -> str:
        """แปลง Brain ID เป็น Mesh IP — ต้องทำภายใน 2ms"""
        pass
```

### MDR Routing Engine
```python
class MeshDistributedRouter:
    ALPHA = 0.5   # Noise weight
    BETA  = 0.3   # Distance weight
    GAMMA = 0.2   # Battery weight

    def calculate_cost(self, noise: float, distance: float, battery: float) -> float:
        return (self.ALPHA * noise) + (self.BETA * distance) + (self.GAMMA * battery)

    def find_optimal_path(self, source: str, destination: str) -> list:
        """Modified Dijkstra — คืนเส้นทางที่ Total Cost ต่ำสุด"""
        pass

    def update_routing_table(self, node_id: str, status: str):
        """อัปเดตสถานะโหนด — Self-Healing เมื่อโหนดหาย"""
        pass
```

### NPI Bio-Signature Validator
```python
class NeuralPrivacyFilter:
    def validate_bio_signature(self, packet, expected_signature) -> bool:
        """ตรวจสอบ EEG Pattern เฉพาะบุคคล"""
        pass

    def apply_firewall_rules(self, packet) -> str:
        """คืนค่า: PASS / BLOCK / RATE_LIMIT / DROP_AND_LOG"""
        pass

    def log_violation(self, packet, rule_id: str):
        """บันทึกการละเมิดกฎ NPI"""
        pass
```

---

## 4.5 Bug Report Template

```
ID: NE-[ลำดับ]
Severity: Critical (ระบบล่ม) / High (ส่งข้อมูลผิด) / Medium / Low (แสดงผลเพี้ยน)
Component: [NNAP / MDR / NPI / Simulation]
Description: รายละเอียดปัญหา

Steps to Reproduce:
  1. รันโหนด A...
  2. เพิ่ม Noise...
  3. ตรวจ Routing Table

Expected: ระบบต้องสลับไปใช้โหนด B
Actual:   ระบบค้างที่โหนด A จน Time-out
Status:   Open / In Progress / Resolved
```

---

## 4.6 Presentation Structure (วันนำเสนอ)

| Section | เวลา | ผู้นำเสนอ |
|---|---|---|
| Introduction — Project Vision | 2 นาที | ปิยพันธ์ (Architect) |
| Architecture — Neuro-Layer Design | 3 นาที | ปิยพันธ์ (Architect) |
| Implementation — BCI & Mesh Protocols | 4 นาที | วรปรัชญ์ (Engineer) |
| Neuro-Security — NPI Filter | 3 นาที | เนติภัทร (Specialist) |
| Demo — Simulation Video | 5 นาที | วรปรัชญ์ (Engineer) |
| Testing Results — Latency & Accuracy | 2 นาที | วรปรัชญ์ (Tester) |
| Conclusion & Q&A | 1 นาที | DevOps |

---

*NeuroEdge Mesh Network | CP352005 Networks | Sprint-01: First Whisper | 2026-02-23 to 2026-03-20*
