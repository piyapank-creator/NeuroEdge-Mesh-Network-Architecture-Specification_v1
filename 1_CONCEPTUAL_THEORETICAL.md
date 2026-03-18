# 🧠 NeuroEdge Mesh Network
## 1. CONCEPTUAL & THEORETICAL FOUNDATION

> **Course:** CP352005 Networks | **Sprint-01:** "First Whisper" | **Team:** NeuroEdge

---

## 1.1 Project Vision — วิสัยทัศน์โครงการ

**NeuroEdge Mesh Network** คือสถาปัตยกรรมเครือข่ายที่ผสาน 3 เทคโนโลยีเข้าด้วยกัน:

| เทคโนโลยี | บทบาทในระบบ |
|---|---|
| **Brain-Computer Interface (BCI)** | รับสัญญาณไฟฟ้าจากสมองมนุษย์โดยตรงผ่าน EEG Headset |
| **Edge Computing** | ประมวลผลข้อมูลที่ "ขอบเครือข่าย" เพื่อลด Latency ให้ต่ำสุด |
| **Mesh Network** | โครงข่ายไร้ศูนย์กลาง ทุกโหนดเชื่อมต่อกันได้โดยตรง ไม่ต้องพึ่ง Infrastructure |

**เป้าหมายหลัก:** ให้มนุษย์สื่อสารกับระบบดิจิทัลได้โดยตรงผ่านคลื่นสมอง โดยไม่ต้องพึ่งพาอุปกรณ์ Input แบบดั้งเดิม (คีย์บอร์ด, เมาส์, หน้าจอสัมผัส)

> **KEY INSIGHT:** NeuroEdge ไม่ใช่แค่การทำ BCI ธรรมดา แต่เป็นการออกแบบ **"เครือข่ายที่มีสมองเป็นโหนด" (Brain as a Network Node)** ซึ่งต้องการโปรโตคอลใหม่ทุกชั้น ตั้งแต่ Physical Layer ไปจนถึง Application Layer

---

## 1.2 ปัญหาหลักที่โปรเจกต์แก้ (Problem Statement)

- **ข้อจำกัดอุปกรณ์ Input:** มนุษย์ต้องการสื่อสารโดยไม่ใช้มือ เช่น นักดำน้ำ, ทหาร, ผู้ได้รับบาดเจ็บ
- **Latency สูง:** ระบบ BCI ทั่วไปมี Latency สูงเกิน 100ms ไม่เหมาะกับ Real-time Use
- **ความเป็นส่วนตัวของความคิด:** สัญญาณสมองต้องมีการป้องกันไม่ให้ถูกดักจับหรือปลอมแปลง
- **Connectivity ในพื้นที่ห่างไกล:** Mesh Network ช่วยให้สื่อสารได้แม้ไม่มีโครงสร้างพื้นฐาน

---

## 1.3 Use Cases หลัก 3 รูปแบบ

| Use Case | คำอธิบาย | บริบทการใช้งาน |
|---|---|---|
| **🗨️ Thought-to-Text Messenger** | พิมพ์ข้อความผ่านความคิด ไม่ต้องใช้มือ | พื้นที่ไม่มีสัญญาณมือถือ |
| **🆘 Emergency Brain-Beacon** | ส่งสัญญาณขอความช่วยเหลือ + GPS อัตโนมัติเมื่อผู้ใช้ตกใจหรือบาดเจ็บ | สถานการณ์ฉุกเฉิน |
| **🤝 Collaborative Mesh Mind** | ทีมกู้ภัยแชร์ความรู้สึก / ภาพที่เห็น ผ่านเครือข่าย Mesh | ภารกิจทีมกู้ภัย |

---

## 1.4 Educational Objectives — จุดประสงค์การเรียนรู้

โปรเจกต์นี้ออกแบบมาให้นักศึกษาประยุกต์ใช้ความรู้ใน 3 ด้าน:

1. **Mesh Topology** — ออกแบบโครงสร้างเครือข่ายแบบไร้ศูนย์กลาง (Decentralized)
2. **Edge Computing** — ลดค่าความหน่วงด้วยการประมวลผลใกล้แหล่งข้อมูล
3. **Protocol Design** — ออกแบบโปรโตคอลที่แปลงสัญญาณสมองเป็น Digital Packet

---

## 1.5 Theoretical Background — พื้นฐานทฤษฎีที่เกี่ยวข้อง

### 1.5.1 Brain-Computer Interface (BCI)
สัญญาณสมองที่ระบบใช้มี 3 ประเภทหลัก:

| คลื่น | ความถี่ | ความหมาย |
|---|---|---|
| **Alpha** | 8–12 Hz | สมาธิ, ผ่อนคลาย |
| **Beta** | 13–30 Hz | ตื่นตัว, โฟกัส |
| **Gamma** | 30+ Hz | ประมวลผลข้อมูลระดับสูง |

### 1.5.2 Mesh Network Theory
- **Topology:** ทุกโหนดเชื่อมกันได้โดยตรง ไม่มีจุดล้มเหลวเดี่ยว (Single Point of Failure)
- **Self-Healing:** เมื่อโหนดหาย เส้นทางใหม่คำนวณอัตโนมัติ
- **Scalability Challenge:** ยิ่งโหนดมากขึ้น ความซับซ้อนของ Routing เพิ่มแบบ Exponential

### 1.5.3 Edge Computing Principle
- ประมวลผลข้อมูล ณ จุดที่ใกล้ที่สุดกับแหล่งที่มา
- ลด Round-trip Time ไปยัง Cloud ส่วนกลาง
- เหมาะกับ Use Case ที่ต้องการ Latency < 50ms

### 1.5.4 Neuroethics Foundation
อ้างอิงจาก Nita A. Farahany, *"The Battle for Your Brain"* — หลักการสำคัญ:
- **Cognitive Liberty:** สิทธิของบุคคลในการควบคุมความคิดของตนเอง
- **Mental Privacy:** ข้อมูลจากสมองต้องได้รับการปกป้องเช่นเดียวกับข้อมูลส่วนบุคคล
- **Neural Integrity:** ห้ามมีการแทรกแซงหรือดัดแปลงสัญญาณสมองโดยไม่ได้รับอนุญาต

---

## 1.6 Neural Dissonance — ผลกระทบเมื่อ Latency สูงเกินไป

> **Neural Dissonance** คือภาวะที่ผู้ใช้รับข้อมูลผิดจังหวะ เกิดขึ้นเมื่อ Latency สูงเกิน **50ms** ส่งผลให้เกิดอาการมึนงงหรือสับสน

นี่คือเหตุผลว่าทำไม target ของระบบจึงต้องการ **Latency < 50ms** อย่างเคร่งครัด

---

## 1.7 Glossary — คำศัพท์พื้นฐาน

| Term | คำจำกัดความ |
|---|---|
| **NNAP** | Neuro-Node Addressing Protocol: โปรโตคอลกำหนดที่อยู่โหนดสมองแบบ 24-byte |
| **MDR** | Mesh Distributed Routing: อัลกอริทึมเส้นทางกระจายศูนย์ที่ใช้ Noise + Latency เป็นเกณฑ์ |
| **NPI** | Neuro-Privacy & Integrity: ระบบคัดกรองจริยธรรมและปกป้องความเป็นส่วนตัวของคลื่นสมอง |
| **BSP** | Bio-Sync Protocol: โปรโตคอล Session Layer รักษาเสถียรภาพการเชื่อมต่อสมอง-ระบบ |
| **Bio-Signature** | เอกลักษณ์เฉพาะตัวของคลื่นสมองรายบุคคล ใช้ยืนยันตัวตน |
| **Thought Packet** | หน่วยข้อมูลที่บรรจุสัญญาณสมองที่ถูกแปลงและ Serialize แล้ว |
| **SNR** | Signal-to-Noise Ratio: อัตราส่วนสัญญาณต่อสัญญาณรบกวน ยิ่งสูงยิ่งดี |
| **Edge Node** | โหนด Mesh ที่ทำหน้าที่ประมวลผลข้อมูลใกล้แหล่งที่มา เพื่อลด Latency |
| **Emotional Vector** | ค่า Valence + Arousal แนบไปกับ Packet เพื่อระบุสภาวะอารมณ์ผู้ส่ง |
| **Neural Dissonance** | ภาวะสับสนเมื่อ Latency สูงเกิน 50ms ส่งผลให้ผู้ใช้มึนงง |

---

## 1.8 References

- Kurose & Ross, *"Computer Networking: A Top-Down Approach"* — Layered Architecture Design
- Tanenbaum, *"Computer Networks"* — Distributed Routing Theory
- Nita A. Farahany, *"The Battle for Your Brain"* — Cognitive Liberty & Neuroethics (NPI Design)
- OSI Model — ISO/IEC 7498-1: มาตรฐาน 7-Layer ที่นำมาประยุกต์ใช้
- PhysioNet / MIMIC Databases — EEG Baseline Data สำหรับ ML Classifier

---

*NeuroEdge Mesh Network | CP352005 Networks | Sprint-01: First Whisper | 2026-02-23 to 2026-03-20*
