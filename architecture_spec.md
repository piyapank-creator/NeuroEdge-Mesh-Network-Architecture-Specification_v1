# **NeuroEdge Mesh Network Architecture Specification v1.0**

**Architectural Review Document \- Course CP352005 Networks**

| Version | Date | Author | Role | Changes |
| :---- | :---- | :---- | :---- | :---- |
| v1.0 | 22/02/2026 | NeuroEdge Mesh Network | Implementation Committee | Initial architectural design based on Neuro-Mesh |

TEAM ROLE

| Role | Name | Responsibilities |
| :---- | :---- | :---- |
| Architect | นาย วรปรัชญ์ พิมพ์อุบล | ออกแบบระบบโดยรวม, นิยาม Layer, การเชื่อมต่อระหว่าง BCI และเครือข่าย |
| Engineer | นาย วรปรัชญ์ พิมพ์อุบล | พัฒนาโปรโตคอลแปลงสัญญาณสมอง (BCI Encoding) และอัลกอริทึม Edge Computing |
| Specialist | นาย เนติภัทร ภูครองเพชร | ออกแบบ Mesh Routing และการสื่อสารไร้พรมแดน |
| DevOps | นาย ปิยพันธ์ แก้วเก็บค่า | จัดการ GitHub, สภาพแวดล้อมการจำลองระบบ และ CI/CD |
| Tester/QA | นาย ปิยพันธ์ แก้วเก็บค่า | ทดสอบความหน่วง (Latency) และความถูกต้องของคำสั่งจากสมอง |

## **Part 1: Executive Summary**

### **1.1 Project Vision**

**NeuroEdge Mesh Network** คือสถาปัตยกรรมเครือข่ายที่ผสานเทคโนโลยี Brain-Computer Interface (BCI) เข้ากับ Edge Computing และ Mesh Network เพื่อให้มนุษย์สามารถสื่อสารกับระบบดิจิทัลได้โดยตรงผ่านคลื่นสมอง ลดข้อจำกัดด้านอุปกรณ์อินพุตและเพิ่มประสิทธิภาพในการสื่อสารแบบเรียลไทม์

### **1.2 Educational Objectives**

* ประยุกต์ใช้ความรู้เรื่อง **Mesh Topology** ในการออกแบบโครงสร้างเครือข่ายแบบไร้ศูนย์กลาง  
* ศึกษาการทำงานของ **Edge Computing** ในการลดค่าความหน่วง (Latency) ของข้อมูล  
* ออกแบบโปรโตคอลการรับส่งข้อมูลที่แปลงจากสัญญาณสมอง (Neural Signals)

`## Part 2: Architectural Review`

`### 2.1 Architecture Overview`

| Layer | Protocol / Function | Description |
| :---- | :---- | :---- |
| **Application** | Human-AI Interaction | การควบคุมหรือสั่งงานระบบดิจิทัลโดยตรงผ่านสัญญาณสมอง |
| **Presentation** | Neural Data Serialization | การแปลงและเข้ารหัสสัญญาณสมองเป็นข้อมูลดิจิทัล |
| **Session** | Neural Sync Protocol (NSP) | การรักษาเสถียรภาพของการเชื่อมต่อระหว่างสมองและโหนด |
| **Transport** | Neuro-Security Protocol | การยืนยันตัวตนผ่านรูปแบบคลื่นสมองเฉพาะบุคคล |
| **Network** | Neuro-Mesh Routing (NMR) | การหาเส้นทางที่เร็วที่สุด (Latency-based Routing) ใน Mesh |
| **Data Link** | Brain-Node Addressing | การกำหนดที่อยู่ (Addressing) ให้กับโหนดสมองและโหนด Edge |
| **Physical** | BCI Interface | การตรวจจับสัญญาณประสาท (Signal Encoding) |

### **2.2 Layer-by-Layer Architecture Review: NeuroEdge Mesh Network**

#### **2.2.1 Physical Layer (Simulated: BCI Interface)**

**สถานะ: ✅ อนุมัติ (เน้นการจำลองสัญญาณสมอง)**

เปลี่ยนจากการส่งข้อมูลข้ามเวลา เป็นการรับสัญญาณจาก Brain-Computer Interface (BCI)

| ด้านที่ประเมิน | การประเมิน | หมายเหตุ |
| :---- | :---- | :---- |
| Innovation | High | ใช้เกณฑ์คุณภาพคลื่นสมอง (Signal Quality) แทนระยะทาง |

Python

```
class PhysicalLayer:
    def transmit_neural_signal(self, packet, brain_node_id, edge_node_id):
        """ส่งสัญญาณจากสมองไปยังโหนดขอบ (Edge Node)"""
        # จำลอง: คืนค่าความสำเร็จ/ล้มเหลว ตามคุณภาพสัญญาณ (Brainwave Stability)
        
    def receive_at_edge(self, node_address):
        """รับข้อมูลที่ Edge Node เพื่อเตรียมประมวลผล"""
```

#### **2.2.2 Data Link Layer \- Neuro-Node Addressing Protocol (NNAP)**

**สถานะ: ✅ อนุมัติ**

เปลี่ยนจากพิกัดเวลา (Temporal T) เป็น **พิกัดชีวภาพและตำแหน่งโหนด**

**โครงสร้าง Address (24 bytes):**

| Field | Size | Description |
| :---- | :---- | :---- |
| **User ID** | 8B | รหัสประจำตัวเฉพาะของสมองผู้ใช้ (Unique Brain Signature) |
| **Spatial GPS** | 8B | พิกัดตำแหน่งปัจจุบัน (X, Y, Z) สำหรับการระบุโหนดใน Mesh |
| **Signal Type** | 4B | ประเภทคลื่นสมองที่ใช้งาน (เช่น Alpha, Beta, Gamma) |
| **Neuro-Health** | 4B | ค่าความเสถียรของสัญญาณและสถานะการเชื่อมต่อ (Link Stability) |

#### **2.2.3 Network Layer \- Mesh Distributed Routing (MDR)**

**สถานะ: ⚠️ อนุมัติแบบมีเงื่อนไข**

เปลี่ยนจากอัลกอริทึมข้ามเวลา เป็นการหาเส้นทางในเครือข่าย Mesh ที่เคลื่อนที่ตลอดเวลา

**อัลกอริทึม:**

Cost \= α\*SignalNoise \+ β\*NodeDistance \+ γ\*EnergyLevel

* **α (Noise):** 0.5 (เน้นความชัดเจนของความคิด)  
* **β (Distance):** 0.3 (ระยะห่างระหว่างโหนด Mesh)  
* **γ (Energy):** 0.2 (พลังงานแบตเตอรี่ของอุปกรณ์สวมใส่)

  #### **2.2.4 Transport Layer \- Neural Privacy & Integrity (NPI)**

**สถานะ: ✅ อนุมัติ**

เปลี่ยนจาก "การป้องกัน Paradox" เป็น **"การป้องกันการบุกรุกสมองและความถูกต้องของคำสั่ง"**

| Rule ID | Description | Action |
| :---- | :---- | :---- |
| **R001** | **Unauthorized Access** | **Block & Alert** |
| **R002** | **Signal Distortion** | **Request Retransmit** |
| **R003** | **Command Buffer Overflow** | **Rate Limit** |

**2.2.5 Session Layer \- Bio-Sync Protocol (BSP)**

**สถานะ: ✅ อนุมัติ**

จัดการเซสชันการเชื่อมต่อระหว่าง "สมอง" กับ "ระบบ Cloud/AI" ให้เสถียร

**Session States:**

DISCONNECTED → CALIBRATING (จูนคลื่นสมอง) → SYNCED → ACTIVE → STANDBY → CLOSED

#### **2.2.6 Presentation Layer \- Neural Data Translation**

**สถานะ: ✅ อนุมัติ**

แปลง "คลื่นไฟฟ้าสมอง (Raw EEG)" ให้เป็น "ข้อมูลดิจิทัล (JSON/Binary)" ที่คอมพิวเตอร์เข้าใจ

Python

```
class NeuralSerializer:
    def encode_thought(self, brain_waves):
        """แปลงคลื่นสมองเป็นคำสั่งดิจิทัล เช่น 'Move Forward' -> 0x01"""
        
    def decode_to_neural_feedback(self, data):
        """แปลงข้อมูลจากเครือข่ายกลับเป็นสัญญาณกระตุ้นประสาท (ถ้ามี)"""
```

#### **2.2.7 Application Layer \- Neuro-App Suite**

**สถานะ: ✅ อนุมัติ**

โปรแกรมประยุกต์ใช้งานจริง 3 รูปแบบหลัก:

1. **Thought-to-Text Messenger:** พิมพ์ข้อความแชทผ่านความคิดในพื้นที่ที่ไม่มีสัญญาณมือถือ  
2. **Emergency Brain-Beacon:** ส่งสัญญาณขอความช่วยเหลือฉุกเฉินและพิกัด GPS อัตโนมัติเมื่อผู้ใช้ตกใจหรือบาดเจ็บ  
3. **Collaborative Mesh Mind:** การทำงานร่วมกันของทีมกู้ภัยผ่านการแชร์ความรู้สึกหรือภาพที่เห็นผ่านเครือข่าย Mesh  
   - 

### 2.3 Interface Contracts

**Cross-Layer Interfaces:**

**`Cross-Layer Interfaces:`** `การสื่อสารระหว่างชั้น Layer จะใช้มาตรฐาน Request/Confirm/Indicate เพื่อให้ระบบมีความเป็น Modular และสามารถเปลี่ยนอัลกอริทึมภายในได้โดยไม่กระทบ Layer อื่น`

**`โครงสร้างพื้นฐาน:`**

* **`Layer N → Layer N-1:`** `request(service_type, parameters)`  
* **`Layer N-1 → Layer N:`** `confirm(status, result) และ indicate(event, data)`

**Example: Network → Data Link:**

`ในระบบ NeuroEdge เมื่อ Network Layer ต้องการส่งข้อมูลไปยังโหนดเป้าหมาย จะต้องขอที่อยู่ทางกายภาพ (Brain-Node Address) จาก Data Link Layer ดังนี้:`

\# Network layer (MDR) requests address resolution  
data\_link.request("RESOLVE\_NEURO\_ID", {  
    "target\_user\_id": "USER\_BRAIN\_007",  
    "priority": "HIGH",  
    "timeout": 10  
})

\# Data Link layer (NNAP) responds  
data\_link.confirm("SUCCESS", {  
    "neuro\_address": "NA\[ID:007, GPS:13.75,100.50, SIG:ALPHA, STB:0.95\]",  
    "resolution\_time": 0.05  
})

**Example: Physical Layer → Network Layer (Signal Indication)** เมื่ออุปกรณ์ BCI ตรวจพบคลื่นสมองที่มีความเข้มข้นสูงเพียงพอ:

\# Physical layer indicates new data arrival  
network.indicate("SIGNAL\_DETECTED", {  
    "raw\_data\_stream": "0xFFE0...",  
    "signal\_quality": 0.88,  
    "source\_node": "LOCAL\_BCI\_HEADSET"  
})

2.4 Non-Functional Requirements Review

| Requirement | Target (เป้าหมาย) | Current Status (สถานะปัจจุบัน) | Status |
| :---- | :---- | :---- | :---- |
| **Scalability** | Support 20+ Mesh Nodes | 5 Nodes (Simulated) | ⚠️ Needs work |
| **Performance** | \< 100ms End-to-End Latency | \< 50ms (Theoretical) | ✅ Good |
| **Reliability** | 98% Command Accuracy | 90% (Signal Noise issues) | ⚠️ Needs Refinement |
| **Maintainability** | Modular BCI Driver Support | High (Layered Design) | ✅ Good |
| **Security** | 256-bit Bio-Encryption | Fully Specified | 🔄 In progress |

2.5 Security Architecture (Paradox Prevention)  
**Security Zones:**

1. **Personal Neural Zone (PNZ):** พื้นที่เก็บข้อมูลดิบในอุปกรณ์สวมใส่ (BCI Headset) \- **Trusted**  
2. **Neuro-Mesh DMZ:** โหนด Edge ที่ทำหน้าที่กรองสัญญาณและตรวจสอบสิทธิ์ \- **Inspection Zone**  
3. **Public Mesh Cloud:** เครือข่ายที่ใช้ส่งข้อมูลผ่านโหนดอื่นๆ \- **Untrusted (Encrypted)**

**Comparison: Network Security vs. Neuro-Security** | Network Security | NeuroEdge Mesh Security | | :--- | :--- | | Firewall | **Neural Privacy Filter** (กรองความคิดที่ไม่ต้องการแชร์) | | Intrusion Detection (IDS) | **Anomaly Signal Detection** (ตรวจจับคลื่นแทรกแซง) | | Multi-Factor Auth | **Bio-Pattern Matching** (ยืนยันตนด้วยลายเซ็นสมอง) | | VPN Tunnel | **Neural Tunneling** (เข้ารหัสคลื่นสมองระหว่างโหนด) |

---

## Part 3: บันทึกการตัดสินใจเชิงสถาปัตยกรรม (Architecture Decisions Log)

**Decision 1: การเลือกใช้ Python สำหรับจำลองระบบ BCI-Mesh**

* **บริบท:** ทีมมีสมาชิก 3 คน (วรปรัชญ์, เนติภัทร, ปิยพันธ์) จึงต้องการเครื่องมือที่ทุกคนสามารถช่วยกัน Code และทดสอบได้เร็ว  
* **การตัดสินใจ:** ใช้ Python เป็นหลักในการเขียน Logic ของทุก Layer  
* **ผลกระทบ:** ทำให้สามารถทำ Demo ส่วนการแปลคำสั่งสมอง (Presentation Layer) ได้เห็นภาพชัดเจนกว่าการใช้โปรแกรมจำลองเครือข่ายเพียวๆ

**Decision 2: การใช้ระบบที่อยู่แบบ 24-Byte (NNAP)**

* **บริบท:** เครือข่าย Mesh แบบเคลื่อนที่ (Mobile Mesh) ต้องการที่อยู่ที่ระบุได้มากกว่าแค่ ID ของเครื่อง  
* **การตัดสินใจ:** ออกแบบ Address ให้ประกอบด้วย 4 ส่วน: `[User_ID(8) | GPS(8) | Wave_Type(4) | Stability(4)]`  
* **เหตุผล:** ข้อมูล **Stability** ในที่อยู่ช่วยให้ระบบตัดโหนดที่ "สมาธิหลุด" หรือ "สัญญาณขาด" ออกจากเส้นทางได้อัตโนมัติ

**Decision 3: อัลกอริทึมเส้นทางถ่วงน้ำหนัก (Weighted Cost Routing)**

* **บริบท:** ต้องเลือกว่าจะส่งข้อมูลผ่านใครดีในเครือข่าย Mesh  
* **สูตรคำนวณ:** $Cost \= (0.5 \\times Noise) \+ (0.3 \\times Distance) \+ (0.2 \\times Battery)  
* **เงื่อนไขการอนุมัติ (Required Changes):** สัปดาห์ที่ 3 ทีมต้องทดสอบว่าหากตั้งค่า Noise ไว้สูงเกินไป ระบบจะหาเส้นทางเจอหรือไม่ (Convergence Analysis)

---

## Part 4: Architectural Review Sign-off

| Role | Name | Signature | Date | Comments |
| :---- | :---- | :---- | :---- | :---- |
| **Architect** | นาย วรปรัชญ์ พิมพ์อุบล |  | 22/02/2026 |  |
| **Engineer** | นาย วรปรัชญ์ พิมพ์อุบล |  | 22/02/2026 |  |
| **Specialist** | นาย เนติภัทร ภูครองเพชร |  | 22/02/2026 |  |
| **DevOps** | **นาย ปิยพันธ์ แก้วเก็บค่า** |  | 22/02/2026 |  |
| **Tester/QA** | **นาย ปิยพันธ์ แก้วเก็บค่า** |  | 22/02/2026 |  |

**Review Outcome:** ⚠️ Conditional Approval  
**Conditions to be met by:** Week 2, Day 3  
**Conditions:**

1. ต้องระบุค่าพารามิเตอร์ α, β, γ ในอัลกอริทึม MDR ให้ชัดเจนในการทดลองสัปดาห์ที่ 2  
2. ต้องมีระบบสำรอง (Fall-back) เมื่อคุณภาพคลื่นสมองต่ำกว่า 50%

---

# **Appendices**

### **Appendix A: Glossary** 

| Term | Definition |
| :---- | :---- |
| **NNAP** | Neuro-Node Addressing Protocol: โปรโตคอลกำหนดที่อยู่โหนดสมองแบบ 24-byte |
| **MDR** | Mesh Distributed Routing: อัลกอริทึมการเลือกเส้นทางแบบกระจายศูนย์ที่ใช้ค่า Noise และ Latency เป็นเกณฑ์ |
| **NPI** | Neuro-Privacy & Integrity: ระบบคัดกรองจริยธรรมและปกป้องความเป็นส่วนตัวของข้อมูลคลื่นสมอง |
| **Neural Dissonance** | ภาวะการรับข้อมูลผิดจังหวะที่เกิดจากความหน่วง (Latency) สูงเกิน 50ms ส่งผลให้ผู้ใช้เกิดอาการมึนงงหรือสับสน |
| **Bio-Signature** | เอกลักษณ์เฉพาะตัวของคลื่นสมองรายบุคคลที่ใช้ในการยืนยันตัวตนก่อนเข้าสู่เครือข่าย |
| **Emotional Vector** | ค่าตัวแปร Valence และ Arousal ที่แนบไปกับข้อมูลเพื่อระบุสภาวะอารมณ์ของผู้ส่ง |

Appendix B: References 

**Kurose & Ross**, *"Computer Networking: A Top-Down Approach"* – สำหรับการออกแบบโครงสร้าง Layered Architecture  
**Tanenbaum**, *"Computer Networks"* – สำหรับทฤษฎีการจัดการ Routing ในระบบ Distributed Systems  
**Nita A. Farahany**, *"The Battle for Your Brain"* – สำหรับหลักการ Cognitive Liberty และพื้นฐานด้าน Neuroethics ที่ใช้ใน NPI  
**OSI Model \- ISO/IEC 7498-1** – มาตรฐานการแบ่งชั้นเลเยอร์ที่นำมาประยุกต์ใช้กับ 7-Layer Neuro-Mesh  
**PhysioNet / MIMIC Databases** – แหล่งข้อมูล EEG Baseline สำหรับการเทรน ML Classifier

---

*This architectural specification is approved for the CP352005 Networks undergraduate project.*

