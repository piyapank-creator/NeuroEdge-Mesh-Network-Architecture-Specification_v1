# ⚙️ NeuroEdge Mesh Network
## 3. IMPLEMENTATION & DEPLOYMENT — Overview & Integration

> **Course:** CP352005 Networks | **Sprint-01:** "First Whisper" | **Team:** NeuroEdge

---

## 3.1 Sprint Overview

| Attribute | Detail |
|---|---|
| **Sprint Name** | Sprint-01: "First Whisper" (Neuro-Mesh Foundation) |
| **Duration** | 4 Weeks — 20 Working Days (2026-02-23 to 2026-03-20) |
| **Primary Goal** | สร้างโครงข่ายประสาทจำลอง (Neuro-Mesh) เพื่อทดสอบโปรโตคอล NNAP และ MDR ภายใต้ Latency < 50ms |
| **Secondary Goal** | ยืนยันว่าระบบ NPI สามารถบล็อกสัญญาณรบกวนและรักษาความปลอดภัยของ Bio-Signature ได้แม่นยำ |

---

## 3.2 Complexity & Effort Assessment

| Component | ความยาก (1–5) | Risk | Effort (hours) |
|---|---|---|---|
| BCI Encoding (NNAP) | ⭐⭐⭐⭐⭐ 5 | HIGH | 25–30 |
| Mesh Distributed Routing (MDR) | ⭐⭐⭐⭐ 4 | HIGH | 20–25 |
| Neural Privacy Filter (NPI) | ⭐⭐⭐ 3 | MEDIUM | 12–15 |
| Simulation Framework (Python) | ⭐⭐⭐⭐ 4 | MEDIUM | 15–20 |
| GUI Visualization | ⭐⭐⭐ 3 | LOW | 10–12 |

**Total Estimated:** 82–120 person-hours
**Available:** 120 hours (4 weeks × 3 members × ~10 hrs/week)
**Buffer:** 18–38 hours (~16–33%)

---

## 3.3 Critical Path & Dependencies

```
Week 1              Week 2              Week 3              Week 4
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Architecture │ → │  Protocols  │ → │ Integration  │ → │ Final Demo  │
│   Design    │    │Implementation│   │  & Testing  │    │ & Delivery  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ↓                  ↓                  ↓                  ↓
  NNAP Spec   →     NNAP Code    →     NNAP Test    →     NNAP Final
  MDR Spec    →     MDR Code     →     MDR Test     →     MDR Final
  NPI Spec    →     NPI Code     →     NPI Test     →     NPI Final
  Sim Setup   →     Sim Dev      →     Sim Test     →     Sim Final
```

**Critical Path:** BCI Encoding → MDR Implementation → System Integration → Latency Testing
**Parallel Tasks:** DevOps Environment Setup + UI Visualization Design

---

## 3.4 Sprint Backlog — Epic & Story Points

### Epic 1: NNAP (Owner: ปิยพันธ์ — Architect)

| Ticket | User Story | Points | Acceptance Criteria |
|---|---|---|---|
| **101** | โครงสร้าง NNAP 24-byte (GPS + User ID) | 5 | NeuroNodeAddress รองรับ GPS + ID + การเข้ารหัส |
| **102** | Algorithm Resolution: Brain ID → Mesh IP | 3 | Lookup ถูกต้อง, Resolution < 2ms |

### Epic 2: MDR (Owner: วรปรัชญ์ — Engineer)

| Ticket | User Story | Points | Acceptance Criteria |
|---|---|---|---|
| **201** | Dijkstra Routing คำนวณจาก Noise + Distance | 8 | สูตร Cost = α(Noise)+β(Dist)+γ(Energy) ใช้งานได้ |
| **202** | Route Caching สำหรับ Edge Nodes | 5 | Cache 100 เส้นทาง, ลดเวลาคำนวณ 50% |

### Epic 3: NPI (Owner: เนติภัทร — Specialist)

| Ticket | User Story | Points | Acceptance Criteria |
|---|---|---|---|
| **301** | Firewall 5 กฎ กรอง Thought ที่ไม่อนุญาต | 5 | NPI Rulebook + ระบบดักจับ Thought Packet ผิดปกติ |
| **302** | Bio-Signature Validation | 8 | ตรวจ EEG เฉพาะบุคคล, บล็อกถ้า Signature ไม่ตรง |

---

## 3.5 Tech Stack

| Component | Technology | หน้าที่ |
|---|---|---|
| Simulation Engine | Python 3.8+ | Logic หลักของทุก Layer |
| Graph / Network | NetworkX | สร้าง Mesh Graph, หาเส้นทาง Dijkstra |
| Numerical Computing | NumPy | คำนวณ SNR, Noise Metrics |
| Visualization | Matplotlib | แสดงผลกราฟ Mesh Network |
| Version Control | GitHub | เก็บ Code + ทำ CI/CD |
| CI/CD | GitHub Actions | Run Unit Tests อัตโนมัติทุก Push |
| Testing | pytest | Automated Unit/Integration Testing |
| Documentation | Markdown / PDF | README + เล่มรายงาน |

---

## 3.6 Test Strategy — 3 Levels

| ระดับ | เมื่อไหร่ | รายละเอียด | เป้าหมาย |
|---|---|---|---|
| **Unit Tests** | Week 2 | ทดสอบฟังก์ชันย่อย: SNR Calc, Address Conversion | > 30 test cases, > 80% coverage |
| **Integration Tests** | Week 3 | ทดสอบข้ามเลเยอร์: Layer 4→1, Routing เมื่อโหนดหาย | > 15 scenarios |
| **System Tests** | Week 4 | รัน Use Case จริง: กู้ภัยห่างไกล, Node Failure | 3 use cases, Latency < 50ms |

**Test Matrix:**

| Component | Unit | Integration | System | Owner |
|---|---|---|---|---|
| NNAP (Addressing) | 10 | 4 | 2 | ปิยพันธ์ |
| MDR (Routing) | 15 | 6 | 3 | ปิยพันธ์ |
| NPI (Transport) | 10 | 5 | 2 | ปิยพันธ์ |
| Thermal / Safety | 5 | 2 | 2 | ปิยพันธ์ |

---

## 3.7 RACI Matrix

| Activity | ปิยพันธ์ | วรปรัชญ์ | เนติภัทร |
|---|---|---|---|
| Architecture Design | **A/R** | C | C |
| Core Implementation | I | **A/R** | C |
| Privacy Rule Engine (NPI) | C | R | **A/R** |
| Environment & CI/CD | **A/R** | C | — |
| Testing & QA | C | **A/R** | I |
| Final Submission | **A/R** | R | R |

> R = Responsible | A = Accountable | C = Consulted | I = Informed

---

## 3.8 Definition of Ready (DoR) & Definition of Done (DoD)

### Definition of Ready (DoR) — ก่อนเริ่มทำงาน
- **Interface Contract:** โครงสร้างรับ-ส่งข้อมูล (Parameters & Return Types) ต้องนิ่งก่อนเริ่ม Code
- **Architecture Compliance:** ปิยพันธ์ตรวจว่า Task สอดคล้องกับโครงสร้าง 7 ชั้น
- **Dev-Environment Ready:** Python/NetworkX ติดตั้งและทดสอบพร้อมใช้งาน
- **Specialist Sign-off:** กฎ NPI ต้องผ่านการรับรองจากเนติภัทรก่อนเขียน Firewall
- **Complexity Estimated:** ทุก Task ต้องมี Story Points และผู้รับผิดชอบหลัก

### Definition of Done (DoD) — สิ้นสุดงาน
- **Build Passes:** โค้ดผ่านการ compile ไม่มี Syntax/Fatal Error
- **Latency Respect:** โมดูลใหม่ต้องไม่ทำให้ระบบช้าเกิน 50ms
- **Peer Reviewed:** ผ่านการตรวจจากเพื่อนอย่างน้อย 1 คน
- **Documented:** มี Docstring ในฟังก์ชันสำคัญ + README.md ตาม PEP 8
- **Integration Verified:** Module ใหม่ทำงานร่วมกับระบบเดิมได้โดยไม่ขัดแย้ง

---

## 3.9 Success Criteria Sign-off

| Milestone | Target | Owner | Status |
|---|---|---|---|
| Blueprint & Spec Approved | Week 1 | Architect | ⏳ Pending |
| Core Protocol Implementation | Week 2 | Engineer | ⏳ Pending |
| Mesh Stability & Visualization | Week 3 | DevOps | ⏳ Pending |
| Multi-Scenario Simulation | Week 3 | All Members | ⏳ Pending |
| Bio-Safety & Precision Final Tests | Week 4 | Tester/QA | ⏳ Pending |
| Final Delivery & Presentation | Week 4 | All Members | ⏳ Pending |

---

## 3.10 Escalation Protocol

| ประเภทปัญหา | ขั้นตอน |
|---|---|
| ปัญหาโค้ด / Bug | วรปรัชญ์แก้เอง 4 ชั่วโมง → ปรึกษาปิยพันธ์ว่ากระทบโครงสร้างไหม |
| ปัญหากฎจริยธรรม | เนติภัทรตัดสินใจ → วรปรัชญ์ Implement → ปิยพันธ์ตรวจ Interface |
| ปัญหา Merge ไม่ได้ | ปิยพันธ์ (DevOps) เข้ามา Lead แก้ปัญหาทันที |

---

*NeuroEdge Mesh Network | CP352005 Networks | Sprint-01: First Whisper | 2026-02-23 to 2026-03-20*
