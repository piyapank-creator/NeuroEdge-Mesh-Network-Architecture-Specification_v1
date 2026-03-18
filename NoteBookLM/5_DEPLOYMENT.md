# 🚀 NeuroEdge Mesh Network
## 5. DEPLOYMENT — Infrastructure, CI/CD & Operations

> **Course:** CP352005 Networks | **Sprint-01:** "First Whisper" | **Team:** NeuroEdge

---

## 5.1 Infrastructure Requirements

| Component | Technology | Configuration / หน้าที่ |
|---|---|---|
| **Version Control** | GitHub Repository | เก็บ Code + Documents ทั้งหมด |
| **Simulation Engine** | Python 3.8+ | ติดตั้ง networkx, numpy, matplotlib |
| **Testing Framework** | pytest | รัน Unit Test อัตโนมัติ |
| **CI/CD Pipeline** | GitHub Actions | Trigger ทุกครั้งที่ Push code |
| **Dependency Management** | pip + requirements.txt | ให้ทุกคนรัน Code ได้เหมือนกัน |
| **Documentation** | Markdown + PDF | README.md + เล่มรายงาน |

### Environment Setup Commands
```bash
# Clone repository
git clone https://github.com/neuroedge/mesh-network.git

# Install dependencies
pip install -r requirements.txt

# requirements.txt
networkx>=2.8
numpy>=1.21
matplotlib>=3.5
pytest>=7.0
```

---

## 5.2 Branch Strategy

```
main ────────────────────────────────────────── production-ready only
  │
  ├── feature/nnap ──────── NNAP addressing development
  ├── feature/mdr  ──────── MDR routing development
  ├── feature/npi  ──────── NPI security development
  └── hotfix/*     ──────── critical bug fixes
```

**กฎการ Merge:**
- ห้าม push ตรงเข้า `main` — ต้องผ่าน Pull Request เท่านั้น
- ทุก PR ต้องผ่าน Code Review จากสมาชิกอย่างน้อย 1 คน
- ทุก PR ต้องผ่าน CI Tests ก่อน Merge
- **ปัญหา Merge Conflict:** ปิยพันธ์ (DevOps) เข้ามา Lead การแก้ปัญหาทันที

---

## 5.3 CI/CD Pipeline

```
Developer Push Code
        │
        ▼
GitHub Actions Trigger
        │
        ├── Step 1: Checkout code
        ├── Step 2: Setup Python 3.8+
        ├── Step 3: pip install -r requirements.txt
        ├── Step 4: pytest --coverage (Unit Tests)
        ├── Step 5: Check coverage > 80%
        └── Step 6: ✅ Pass → Merge allowed | ❌ Fail → Notify team
```

**GitHub Actions Workflow (`.github/workflows/ci.yml`):**
```yaml
name: NeuroEdge CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Check coverage
        run: coverage report --fail-under=80
```

---

## 5.4 Repository Structure

```
neuroedge-mesh-network/
│
├── README.md                   ← Project overview + setup guide
├── requirements.txt            ← Python dependencies
│
├── src/
│   ├── physical/
│   │   └── bci_interface.py    ← Physical Layer — BCI Signal handling
│   ├── datalink/
│   │   └── nnap.py             ← NNAP — 24-byte addressing
│   ├── network/
│   │   └── mdr.py              ← MDR — Modified Dijkstra routing
│   ├── transport/
│   │   └── npi.py              ← NPI — Privacy & Integrity filter
│   ├── session/
│   │   └── bsp.py              ← BSP — Bio-Sync Protocol
│   ├── presentation/
│   │   └── serializer.py       ← Neural Data Translation
│   └── application/
│       └── neuro_apps.py       ← Thought-to-Text, Brain-Beacon, etc.
│
├── simulation/
│   ├── mesh_simulator.py       ← Virtual Mesh Network
│   └── scenarios/
│       ├── rescue_ops.py       ← Use Case: Emergency Rescue
│       └── node_failure.py     ← Use Case: Node Failure & Recovery
│
├── tests/
│   ├── unit/                   ← Unit tests (Week 2)
│   ├── integration/            ← Integration tests (Week 3)
│   └── system/                 ← System / E2E tests (Week 4)
│
├── docs/
│   ├── architecture_spec.md
│   ├── api.md
│   ├── user_guide.md
│   └── test_report.md
│
└── .github/
    └── workflows/
        └── ci.yml              ← GitHub Actions CI/CD
```

---

## 5.5 Simulation Deployment

### Virtual Mesh Network Setup
```python
import networkx as nx

# สร้าง Mesh Graph จำลอง
mesh = nx.Graph()

# เพิ่มโหนด (Brain Nodes)
nodes = ["BRAIN_A", "BRAIN_B", "BRAIN_C", "EDGE_1", "EDGE_2"]
for node in nodes:
    mesh.add_node(node)

# เพิ่มเส้นเชื่อมพร้อม Cost attributes
mesh.add_edge("BRAIN_A", "EDGE_1", noise=0.2, distance=10, battery=0.9)
mesh.add_edge("BRAIN_B", "EDGE_1", noise=0.3, distance=15, battery=0.7)
mesh.add_edge("EDGE_1",  "EDGE_2", noise=0.1, distance=5,  battery=1.0)
mesh.add_edge("BRAIN_C", "EDGE_2", noise=0.4, distance=12, battery=0.8)
```

### 3 Use Cases ที่ต้องทดสอบใน System Test
1. **Emergency Rescue Scenario:** กู้ภัยในพื้นที่สัญญาณต่ำ — วัด Latency < 50ms
2. **Node Failure & Recovery:** จำลองโหนดล่ม → ระบบ Self-Healing → เส้นทางใหม่
3. **Privacy Attack:** จำลองการโจมตีด้วย Thought Injection → NPI ต้องบล็อกได้

---

## 5.6 Performance Monitoring & Resource Constraints

| Metric | Target | Critical Threshold |
|---|---|---|
| End-to-End Latency | < 50ms | > 100ms = ระบบล้มเหลว |
| Address Resolution Time | < 2ms | > 5ms = ต้อง optimize |
| Route Computation Time | < 10ms | > 20ms = ต้องทบทวน Algorithm |
| Routing Cache Hit Rate | > 50% | < 30% = Cache ไม่มีประสิทธิภาพ |
| Unit Test Coverage | > 80% | < 70% = ไม่ผ่าน CI |
| Signal Stability (STB) | > 0.5 | ≤ 0.5 = ตัดโหนดออก |

**Resource Monitoring:**
- จำลองการใช้ทรัพยากรเครื่องโหนด เพื่อคุม Thermal Limit
- ค่าอุณหภูมิต้องไม่เกินเกณฑ์ที่ Architect กำหนด
- Battery Level ต่ำกว่า 20% → โหนดถูกลดลำดับความสำคัญใน Routing

---

## 5.7 Deployment Documents Checklist

| Document | Owner | ไฟล์ |
|---|---|---|
| User Guide | DevOps (ปิยพันธ์) | `docs/user_guide.md` |
| API Reference | Engineer (วรปรัชญ์) | `docs/api.md` |
| Test Report | Tester (วรปรัชญ์) | `docs/test_report.md` |
| Architecture Final | Architect (ปิยพันธ์) | `architecture_spec.md` |
| Implementation Summary | All | `README.md` |

---

## 5.8 Final Delivery Package

**Day 20 Deliverables:**
- [ ] Source code (GitHub Repository + ZIP)
- [ ] Demo Video (5 นาที — อัดโดย วรปรัชญ์)
- [ ] Presentation Slides
- [ ] Final Test Report (Latency measurements, Coverage report)
- [ ] Architecture Documentation
- [ ] Retrospective: Action Items สำหรับ Phase 2

**Retrospective Topics:**
1. สิ่งที่ทำได้ดี (Keep)
2. สิ่งที่ควรปรับปรุง (Improve)
3. สิ่งที่ค้นพบระหว่างทาง (Learn)
4. Action Items สำหรับ Phase 2

---

## 5.9 Phase 2 — Future Roadmap

| Feature | ความซับซ้อน | Priority |
|---|---|---|
| AI-based Traffic Prediction Routing | High | Medium |
| Dynamic Adaptive Noise Cancellation | High | High |
| Real BCI Hardware Integration (EEG Headset) | Very High | Low (Phase 3) |
| Scalability Test: 20+ Nodes | Medium | High |
| 256-bit Bio-Encryption Implementation | Medium | High |
| Real-time Network Status Dashboard | Medium | Medium |

---

*NeuroEdge Mesh Network | CP352005 Networks | Sprint-01: First Whisper | 2026-02-23 to 2026-03-20*
