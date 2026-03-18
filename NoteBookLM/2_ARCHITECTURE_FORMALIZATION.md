# 🏗️ NeuroEdge Mesh Network
## 2. ARCHITECTURE & FORMALIZATION

> **Course:** CP352005 Networks | **Sprint-01:** "First Whisper" | **Team:** NeuroEdge

---

## 2.1 7-Layer Neuro-OSI Architecture Overview

NeuroEdge ดัดแปลง OSI Model 7 ชั้นให้รองรับ BCI-Mesh โดยแต่ละชั้นมีโปรโตคอลเฉพาะทาง:

| Layer # | ชื่อชั้น | โปรโตคอล / ฟังก์ชัน | สถานะ |
|---|---|---|---|
| **7 — Application** | Neuro-App Suite | Human-AI Interaction (Thought Commands) | ✅ อนุมัติ |
| **6 — Presentation** | Neural Data Translation | Neural Data Serialization (EEG → JSON/Binary) | ✅ อนุมัติ |
| **5 — Session** | Bio-Sync Protocol (BSP) | Neural Sync — รักษาเสถียรภาพเซสชัน | ✅ อนุมัติ |
| **4 — Transport** | Neural Privacy & Integrity (NPI) | Neuro-Security — ยืนยันตัวตนด้วย Bio-Signature | ✅ อนุมัติ |
| **3 — Network** | Mesh Distributed Routing (MDR) | Neuro-Mesh Routing — หาเส้นทาง Latency ต่ำสุด | ⚠️ อนุมัติมีเงื่อนไข |
| **2 — Data Link** | NNAP (Addressing) | Brain-Node Addressing — กำหนดที่อยู่ 24-byte | ✅ อนุมัติ |
| **1 — Physical** | BCI Interface | Signal Encoding — รับสัญญาณประสาทจาก EEG Headset | ✅ อนุมัติ |

---

## 2.2 Layer-by-Layer Detail

### 2.2.1 Physical Layer — BCI Interface ✅
ชั้นล่างสุด รับสัญญาณไฟฟ้าจากสมองผ่าน EEG Headset แปลงเป็นดิจิทัล

- รับสัญญาณ: Alpha (8–12 Hz), Beta (13–30 Hz), Gamma (30+ Hz)
- วัด **Signal Quality** เพื่อประเมินความเสถียรของโหนด
- ส่ง `SIGNAL_DETECTED` Indication ขึ้น Network Layer เมื่อพบสัญญาณใหม่

```python
class PhysicalLayer:
    def transmit_neural_signal(self, packet, brain_node_id, edge_node_id):
        """ส่งสัญญาณจากสมองไปยัง Edge Node — คืนค่าตาม Brainwave Stability"""

    def receive_at_edge(self, node_address):
        """รับข้อมูลที่ Edge Node เพื่อเตรียมประมวลผล"""
```

---

### 2.2.2 Data Link Layer — NNAP ✅
จัดการ Addressing ของ "โหนดสมอง" แต่ละตัว ใช้ฟอร์แมต **24 bytes**

**โครงสร้าง Address:**

| Field | ขนาด | ความหมาย | ตัวอย่าง |
|---|---|---|---|
| **User ID** | 8B | รหัสประจำตัวเฉพาะของสมอง (Unique Brain Signature) | `USER_BRAIN_007` |
| **Spatial GPS** | 8B | พิกัด X, Y, Z ของตำแหน่งโหนดใน Mesh | `13.75, 100.50, 0.0` |
| **Signal Type** | 4B | ประเภทคลื่นสมอง (Alpha / Beta / Gamma) | `ALPHA` |
| **Neuro-Health** | 4B | ค่าความเสถียรของสัญญาณ (Link Stability) | `0.95` |

**ตัวอย่าง Address จริง:**
```
NA[ID:007, GPS:13.75,100.50, SIG:ALPHA, STB:0.95]
```

> **สำคัญ:** ถ้า STB (Stability) ต่ำกว่า 0.5 = สมาธิหลุด / สัญญาณขาด → ระบบตัดโหนดออกจาก Routing Table อัตโนมัติ

- Address Resolution: แปลง Brain ID → Mesh IP ภายใน **< 2ms**
- ตัดโหนดที่มี Neuro-Health ต่ำกว่า Threshold ออกจากเส้นทาง

---

### 2.2.3 Network Layer — MDR ⚠️
หัวใจของระบบ ใช้ **Modified Dijkstra Algorithm** คำนวณเส้นทางที่ดีที่สุดใน Mesh

**สูตรคำนวณ Cost:**
```
Cost = (α × SignalNoise) + (β × NodeDistance) + (γ × EnergyLevel)
```

| Parameter | ค่า Weight | ความหมาย | เหตุผล |
|---|---|---|---|
| **α (Noise)** | 0.5 (50%) | ความชัดเจนของสัญญาณสมอง | Noise มีผลมากที่สุดต่อความน่าเชื่อถือ |
| **β (Distance)** | 0.3 (30%) | ระยะห่างระหว่างโหนด | ระยะไกลเพิ่ม Latency แต่ไม่สำคัญเท่า Noise |
| **γ (Energy)** | 0.2 (20%) | พลังงานแบตเตอรี่อุปกรณ์ | ป้องกันโหนดที่กำลังจะหมดพลังงาน |

**คุณสมบัติ:**
- **Route Caching:** จำ 100 เส้นทางที่ใช้บ่อย เพื่อลดเวลาคำนวณ 50%
- **Self-Healing:** เมื่อโหนดหาย ระบบคำนวณเส้นทางใหม่อัตโนมัติ

**เงื่อนไขการอนุมัติ (Conditional Approval):**
- ต้องระบุค่าพารามิเตอร์ α, β, γ ให้ชัดเจนในการทดลองสัปดาห์ที่ 2
- ต้องทดสอบ **Convergence Analysis** เมื่อ Noise สูงในสัปดาห์ที่ 3
- ต้องมีระบบสำรอง (Fall-back) เมื่อคุณภาพคลื่นสมองต่ำกว่า 50%

---

### 2.2.4 Transport Layer — NPI ✅
ชั้นความปลอดภัย คัดกรองและยืนยัน "Thought Packet" ก่อนส่งขึ้น Session Layer

**กฎ NPI Firewall 5 ข้อ:**

| Rule ID | ชื่อกฎ | เงื่อนไข | Action |
|---|---|---|---|
| **R001** | Unauthorized Access | ไม่มี Bio-Signature ที่ถูกต้อง | Block & Alert |
| **R002** | Signal Distortion | คลื่นสมองถูกปลอมแปลงหรือบิดเบือน | Request Retransmit |
| **R003** | Command Buffer Overflow | ส่งคำสั่งเร็วเกินกว่า Threshold | Rate Limit |
| **R004** | Thought Injection | Pattern ไม่ตรงกับ Bio-Signature เจ้าของ | Drop & Log |
| **R005** | Privacy Violation | ข้อมูลสมองถูกส่งออกโดยไม่ได้รับอนุญาต | Encrypt & Reroute |

**เปรียบเทียบกับ Network Security ปกติ:**

| Network Security | NeuroEdge Security (NPI) |
|---|---|
| Firewall | Neural Privacy Filter (กรองความคิดที่ไม่ต้องการแชร์) |
| IDS (Intrusion Detection) | Anomaly Signal Detection (ตรวจจับคลื่นแทรกแซง) |
| Multi-Factor Auth | Bio-Pattern Matching (ยืนยันตนด้วยลายเซ็นสมอง) |
| VPN Tunnel | Neural Tunneling (เข้ารหัสคลื่นสมองระหว่างโหนด) |

---

### 2.2.5 Session Layer — BSP (Bio-Sync Protocol) ✅
จัดการ State ของการเชื่อมต่อระหว่างสมองกับระบบ Cloud/AI

```
DISCONNECTED → CALIBRATING (จูนคลื่นสมอง) → SYNCED → ACTIVE → STANDBY → CLOSED
```

---

### 2.2.6 Presentation Layer — Neural Data Translation ✅
แปลง **Raw EEG** (คลื่นไฟฟ้าสมอง) ให้เป็น **JSON/Binary** ที่คอมพิวเตอร์เข้าใจ

```python
class NeuralSerializer:
    def encode_thought(self, brain_waves):
        """แปลงคลื่นสมองเป็นคำสั่งดิจิทัล เช่น 'Move Forward' → 0x01"""

    def decode_to_neural_feedback(self, data):
        """แปลงข้อมูลจากเครือข่ายกลับเป็นสัญญาณกระตุ้นประสาท (ถ้ามี)"""
```

---

### 2.2.7 Application Layer — Neuro-App Suite ✅
โปรแกรมประยุกต์ 3 รูปแบบตาม Use Cases ที่ระบุในไฟล์ Conceptual

---

## 2.3 Interface Contracts ระหว่าง Layer

การสื่อสารระหว่าง Layer ใช้มาตรฐาน **Request / Confirm / Indicate** เพื่อให้ระบบเป็น Modular:

- `Layer N → Layer N-1:` `request(service_type, parameters)`
- `Layer N-1 → Layer N:` `confirm(status, result)` และ `indicate(event, data)`

**ตัวอย่าง 1 — Network Layer ขอ Address จาก Data Link Layer:**
```python
# Network layer (MDR) requests address resolution
data_link.request("RESOLVE_NEURO_ID", {
    "target_user_id": "USER_BRAIN_007",
    "priority": "HIGH",
    "timeout": 10
})

# Data Link layer (NNAP) responds
data_link.confirm("SUCCESS", {
    "neuro_address": "NA[ID:007, GPS:13.75,100.50, SIG:ALPHA, STB:0.95]",
    "resolution_time": 0.05   # 50ms
})
```

**ตัวอย่าง 2 — Physical Layer แจ้ง Network Layer ว่าพบสัญญาณใหม่:**
```python
# Physical layer indicates new data arrival
network.indicate("SIGNAL_DETECTED", {
    "raw_data_stream": "0xFFE0...",
    "signal_quality": 0.88,
    "source_node": "LOCAL_BCI_HEADSET"
})
```

---

## 2.4 Security Architecture — 3 โซนความปลอดภัย

| Zone | ชื่อ | Trust Level | หน้าที่ |
|---|---|---|---|
| **Zone 1** | Personal Neural Zone (PNZ) | TRUSTED | เก็บข้อมูลดิบใน BCI Headset — มีแค่เจ้าของเข้าถึง |
| **Zone 2** | Neuro-Mesh DMZ | INSPECTION | Edge Node กรองสัญญาณและตรวจสอบสิทธิ์ก่อนส่งต่อ |
| **Zone 3** | Public Mesh Cloud | UNTRUSTED | เครือข่ายสาธารณะ ข้อมูลต้องถูกเข้ารหัสตลอดเวลา |

---

## 2.5 Non-Functional Requirements

| ด้าน | Target | สถานะ |
|---|---|---|
| **Scalability** | รองรับ 20+ Mesh Nodes | ⚠️ ยังได้แค่ 5 Nodes (จำลอง) |
| **Performance (Latency)** | < 100ms E2E (Target < 50ms) | ✅ ดี (ในทางทฤษฎี) |
| **Reliability** | 98% Command Accuracy | ⚠️ ยังได้ ~90% เพราะ Signal Noise |
| **Security** | 256-bit Bio-Encryption | 🔄 อยู่ระหว่างพัฒนา |
| **Maintainability** | Modular BCI Driver Support | ✅ ดี (Layered Design) |

---

## 2.6 Architecture Decision Log (ADR)

| Decision | บริบท | ผลลัพธ์ |
|---|---|---|
| **ใช้ Python เป็นหลัก** | ทีม 3 คนต้องการเครื่องมือที่ทุกคน Code ได้ | Demo ชัดเจน, NetworkX ช่วย Visualize Graph ได้ดี |
| **NNAP 24-byte Address** | Mobile Mesh ต้องการ Address ที่มีข้อมูลสถานะโหนด | Stability field ช่วยตัดโหนดสมาธิหลุดออกอัตโนมัติ |
| **Weighted Cost Routing** | ต้องเลือกเส้นทางคำนึงถึง Noise + ระยะทาง + พลังงาน | ต้องทดสอบ Convergence เมื่อ Noise สูงในสัปดาห์ที่ 3 |
| **Dijkstra แทน AI Routing** | ลด Technical Debt ในการพัฒนา 4 สัปดาห์ | ง่ายกว่า แต่ไม่สามารถทำนาย Traffic ได้ |

---

*NeuroEdge Mesh Network | CP352005 Networks | Sprint-01: First Whisper | 2026-02-23 to 2026-03-20*
