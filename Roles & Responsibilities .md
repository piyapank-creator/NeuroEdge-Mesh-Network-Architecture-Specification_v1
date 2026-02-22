**NeuroEdge Project: Roles, Responsibilities & Boundaries Matrix**

**1\. Team Role Assignment Table**

| Role | Assigned To | Primary Responsibilities | Decision Authority |
| :---- | :---- | :---- | :---- |
| **Architect & DevOps** | **ปิยพันธ์** | **ออกแบบโครงสร้างระบบ, กำหนด Interface, วางระบบ GitHub & CI/CD** | **การเลือก Tech Stack, โครงสร้างโปรโตคอล, และกระบวนการ Deployment** |
| **Engineer & Tester** | **วรปรัชญ์** | **พัฒนาโปรโตคอล MDR, เขียนโค้ดจำลอง BCI, ทดสอบ Latency & Bugs** | **อัลกอริทึม Logic, โครงสร้างโค้ด, และเกณฑ์การปล่อยผ่าน (Quality Gate)** |
| **Specialist** | **เนติภัทร** | **วิจัยกฎจริยธรรมสมอง, ออกแบบเงื่อนไข NPI (Privacy Filter)** | **นิยามกฎจริยธรรม และเกณฑ์การตัดสินใจของ Firewall** |

**2\. Detailed Responsibility Matrix (By Project Phase)**

| Phase | ปิยพันธ์ (Arch/DevOps) | วรปรัชญ์ (Eng/Tester) | เนติภัทร (Specialist) |
| :---- | :---- | :---- | :---- |
| **Week 1: Foundation** | **ออกแบบเลเยอร์ interfaces, Setup GitHub Repo และ CI Pipeline** | **วิจัย Python/NetworkX, ร่างแผนการทดสอบ (Test Plan Template)** | **วิจัยกฎจริยธรรม และร่างกฎความเป็นส่วนตัว 5 ข้อ** |
| **Week 2: Implementation** | **ตรวจสอบ Code ให้ตรงตาม Spec, จัดการเรื่อง Branching Strategy** | **พัฒนา NNAP และ MDR Routing, เขียน Unit Test (\>80%)** | **พัฒนา Bio-Signature Validation Engine** |
| **Week 3: Integration** | **นำพาการ Integrate ระบบ, ตรวจสอบความเสถียรของ Build** | **รวมโมดูลทั้งหมด, รันระบบจำลอง และทดสอบประสิทธิภาพ Latency** | **ทดสอบเคสเจาะระบบ (Intrusion Scenarios) และแก้ไข Logic** |
| **Week 4: Delivery** | **ตรวจสอบงานสุดท้าย, ทำคู่มือการติดตั้ง (User Guide)** | **ปรับจูน Latency (\<50ms), จัดทำวิดีโอ Demo และผลทดสอบ** | **ตรวจทานความถูกต้องของข้อมูลในเล่มรายงาน** |

**3\. Responsibility Area Matrix (By Component)**

| Component | Design Owner | Implementation | Testing & Quality |
| :---- | :---- | :---- | :---- |
| **NNAP (Addressing)** | **ปิยพันธ์** | **วรปรัชญ์** | **วรปรัชญ์** |
| **MDR (Routing)** | **ปิยพันธ์** | **วรปรัชญ์** | **วรปรัชญ์** |
| **NPI (Privacy Filter)** | **เนติภัทร** | **วรปรัชญ์ \+ เนติภัทร** | **วรปรัชญ์** |
| **CI/CD & Automation** | **ปิยพันธ์** | **ปิยพันธ์** | **ปิยพันธ์** |
| **Visualization** | **ปิยพันธ์** | **วรปรัชญ์** | **วรปรัชญ์** |

**4\. Boundaries of Responsibility (ขอบเขตงาน)**  
 **ปิยพันธ์ (Architect & DevOps Boundaries)**

* **In Scope: การตัดสินใจเชิงโครงสร้าง, การเชื่อมต่อระหว่าง Layer, การจัดการ Repository, การทำ Automate สคริปต์ต่างๆ**  
* **Out of Scope: การเขียน Algorithm เชิงลึกในส่วนของ MDR (วรปรัชญ์ทำ), การลงรายละเอียดกฎจริยธรรม (เนติภัทรทำ)**

### **วรปรัชญ์ (Engineer & Tester Boundaries)**

* **In Scope: การลงมือเขียนโค้ดระบบทั้งหมด, การหาบัค, การวัดผล Latency, การสร้าง Demo Video**  
* **Out of Scope: การตัดสินใจเปลี่ยนสถาปัตยกรรมโดยพลการ (ต้องปรึกษาปิยพันธ์), การกำหนดกฎความปลอดภัยใหม่ (ต้องปรึกษาเนติภัทร)**

**5\. RACI Matrix (Revised)**

| Activity | ปิยพันธ์ | วรปรัชญ์ | เนติภัทร |
| ----- | :---: | :---: | :---: |
| **Architecture Design** | **A/R** | **C** | **C** |
| **Core Implementation** | **I** | **A/R** | **C** |
| **Privacy Rule Engine** | **C** | **R** | **A/R** |
| **Environment & CI/CD** | **A/R** | **C** | **\-** |
| **Testing & QA** | **C** | **A/R** | **I** |
| **Final Submission** | **A/R** | **R** | **R** |

**6\. Communication & Escalation (การแก้ปัญหา)**

* **ปัญหาโค้ด/บัค: วรปรัชญ์ลองแก้เอง 4 ชม. \-\> ปรึกษาปิยพันธ์เพื่อดูว่ากระทบโครงสร้างไหม**  
* **ปัญหากฎจริยธรรม: เนติภัทรตัดสินใจ \-\> วรปรัชญ์นำไป Implement \-\> ปิยพันธ์ตรวจสอบ Interface**  
* **ปัญหาการรวมโค้ดไม่ได้: ปิยพันธ์ในฐานะ DevOps เข้ามา Lead การแก้ปัญหาการ Merge ทันที**

