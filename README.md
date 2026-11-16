<div align="center">

# Viranch Gupta

**Full-Stack Developer · Embedded Systems Builder · HR Technology**

**Full-Stack Engineering · Embedded & IoT Systems · Product Architecture · Fintech**


</div>

## 👋 About Me

Hi, I'm **Viranch Gupta** (`@FinancialNoobster`) — a developer and product builder working at the intersection of **web software, physical devices, workforce technology, and finance**.

I design systems from end to end: **frontend interfaces → backend APIs → databases → authentication and permissions → connected hardware → diagnostics and deployment**. I also work hands-on with **Arduino/ESP32 programming, electronic components, communication protocols, and hardware system design**.

- 🏢 **Building Working Bridge:** an integrated, multi-tenant HR and workforce management platform with connected attendance hardware.
- 🔐 **Engineering interests:** authentication, access control, secure device identity, multi-tenant architecture, and API security.
- 🔧 **Hardware interests:** ESP32/ESP32-S3, Arduino-style C/C++, biometric devices, BLE, RFID, camera modules, TFT screens, and PCB/electronics prototyping.
- 📊 **Analytical approach:** interpreting operational data, designing business workflows, debugging system bottlenecks, and translating requirements into real products.
- 📈 **Beyond software:** fintech, business operations, and building practical tools for organizations.

---

## 🌉 Flagship Project: Working Bridge

> **A connected HR SaaS + attendance hardware ecosystem** — designed to bring workforce operations and physical check-in devices into one platform.

**My work spans product design, full-stack implementation, backend architecture, device integration, and security-aware workflows.** This is an independent product; the full proprietary codebase is not linked from this public profile.

### 🧩 HR platform & business workflows

| Area | What I designed / worked on |
| --- | --- |
| **Multi-role workspaces** | Platform Admin, Founder, HR, Manager, Employee, Freelancer, and delegated Work access |
| **Workforce operations** | Employee lifecycle, onboarding, departments, shifts, attendance, leave balances, holiday calendars, and correction requests |
| **Payroll & finance** | Payroll processing, salary slips, compensation revisions, staff finance, reimbursements, and gratuity workflows |
| **Work & people management** | Projects, tasks, work logs, reviews, recruitment, and approval workflows |
| **Operations & oversight** | Document/asset management, support tickets, notifications, scheduled reminders, reporting dashboards, and audit logs |
| **Commercial platform** | Tenant/company configuration, subscription/billing workflows, and payment integration |

### 🪪 Four types of attendance hardware

| Device / method | What it demonstrates |
| --- | --- |
| **📷 Face recognition terminal** | ESP32-S3 camera integration, TFT interface, image capture, backend recognition, and queued processing using Python/OpenCV |
| **👆 Fingerprint scanner** | Fingerprint device interfacing, enrollment/verification-oriented workflows, and attendance API integration |
| **💳 RFID / card scanner** | Card identifiers, device-to-employee assignments, and authenticated attendance events |
| **📶 Bluetooth attendance device** | BLE communication, browser-device interaction, device assignment, and provisioning flows |

**Also supported in the software:** GPS/location-based and website-based attendance. *Face and fingerprint are biometric methods; RFID and BLE are device-based attendance methods.*

### 🛡️ Security & architecture

- **Identity and access:** JWT-based authentication, HttpOnly authentication cookies, role-based permissions, and scoped dashboards.
- **Web/API protections:** CSRF checks, request validation, CORS configuration, rate limiting, security headers, and audit trails.
- **Device trust:** per-device credentials, hashing/encryption of sensitive device information, and tenant/device association.
- **Provisioning:** factory inventory, device activation claims, and encrypted BLE provisioning workflows.
- **Reliability:** background job queues for face scans, retries, asynchronous email/reminder workers, and diagnostic troubleshooting.
- **Computer vision:** a separate **Python + FastAPI + OpenCV** service using YuNet/SFace components for face detection/recognition.

### 🏗️ How the system fits together

```mermaid
flowchart TD
    A["React + Tailwind HR dashboards"] --> B["Node.js / Express APIs"]
    C["Face / Fingerprint / RFID / BLE devices"] --> D["Device authentication + attendance APIs"]
    D --> B
    E["GPS / web attendance"] --> B
    B --> F[(MongoDB / tenant data)]
    B --> G["Python FastAPI + OpenCV face service"]
    B --> H["Queues · Reports · Reminders · Audit logs"]
```

*Architecture is a high-level view of the application, not a public deployment or security-certification claim.*

---

## 🛠️ Tech Stack

<div align="center">

**Web, UI & Applications**

`JavaScript`
`React`
`Vue.js`
`HTML5`
`CSS3`
`Tailwind CSS`

**Backend, Data & Computer Vision**

`Node.js`
`Express`
`MongoDB`
`Python`
`FastAPI`
`Flask`
`OpenCV`

**Embedded Systems & Connected Hardware**

`Arduino`
`ESP32 / ESP32-S3`
`C++`
`BLE`
`IoT`
`RFID`
`SPI | I2C | UART`

**Engineering & Delivery**

`Git`
`GitHub`
`REST APIs`
`JWT`
`Vercel`
`Render`

</div>

## 🧠 What I Bring to Engineering Projects

| Strength | Example of work |
| --- | --- |
| **Full-stack product development** | Building complete React/Express/MongoDB applications instead of isolated screens |
| **Hardware + software integration** | Connecting microcontrollers, sensors/readers, displays, BLE, and HTTP APIs |
| **System design** | Planning device identity, service boundaries, data models, queues, and multi-tenant workflows |
| **Application security** | Designing login, permissions, device authorization, CSRF defenses, and credential handling |
| **Data & business analysis** | Translating HR/payroll/attendance requirements into reports, rules, and actionable workflows |
| **Debugging & optimization** | Investigating network delays, failed requests, embedded constraints, and backend job reliability |

## 🚀 Projects & GitHub Activity

My public projects, languages, milestones and activity are discovered automatically from GitHub below.

---

## 📊 Live GitHub Dashboard

<!-- LIVE_GITHUB_START -->
> 🔄 Live data initializes when the GitHub Actions workflow runs. Public repository and contribution metrics will refresh hourly.
<!-- LIVE_GITHUB_END -->

## 🤝 Connect

<div align="center">

[`GitHub-FinancialNoobster-171e33?style=for-the-badge&logo=github)](https://github.com/FinancialNoobster`
[`LinkedIn-Viranch Gupta-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/viranch-gupta-99667b18b`

**Building products that connect people, software, and hardware.** ⚡

</div>

<!-- Statistics and activities are generated as GitHub Markdown by the hourly workflow. -->
