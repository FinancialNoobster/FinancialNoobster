<div align="center">

![Viranch Gupta | Full-Stack • Embedded Systems • HR Technology](./assets/banner.svg)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3300&pause=1100&color=41D8D1&center=true&vCenter=true&width=860&lines=Full-Stack+Developer+%7C+Embedded+Systems+Builder;Building+Working+Bridge%3A+HR+SaaS+%2B+Attendance+Devices;ESP32+%7C+Arduino+%7C+APIs+%7C+Security+%7C+System+Design;Turning+real-world+problems+into+connected+products)](https://github.com/DenverCoder1/readme-typing-svg)

**Full-Stack Engineering · Embedded & IoT Systems · Product Architecture · Fintech**

[![Profile views](https://komarev.com/ghpvc/?username=FinancialNoobster&color=6f74e8&style=for-the-badge&label=PROFILE+VIEWS)](https://github.com/antonkomarev/github-profile-views-counter)
[![Followers](https://img.shields.io/github/followers/FinancialNoobster?style=for-the-badge&logo=github&color=24b9aa&labelColor=17213a)](https://github.com/FinancialNoobster?tab=followers)
[![Stars](https://img.shields.io/github/stars/FinancialNoobster?affiliations=OWNER&style=for-the-badge&logo=github&color=8169dc&labelColor=17213a)](https://github.com/FinancialNoobster?tab=repositories)

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

![JavaScript](https://img.shields.io/badge/JavaScript-191f32?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![React](https://img.shields.io/badge/React-191f32?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vue.js](https://img.shields.io/badge/Vue.js-191f32?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![HTML5](https://img.shields.io/badge/HTML5-191f32?style=for-the-badge&logo=html5&logoColor=E34F26)
![CSS3](https://img.shields.io/badge/CSS3-191f32?style=for-the-badge&logo=css&logoColor=1572B6)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-191f32?style=for-the-badge&logo=tailwindcss&logoColor=06B6D4)

**Backend, Data & Computer Vision**

![Node.js](https://img.shields.io/badge/Node.js-191f32?style=for-the-badge&logo=nodedotjs&logoColor=5FA04E)
![Express](https://img.shields.io/badge/Express-191f32?style=for-the-badge&logo=express&logoColor=ffffff)
![MongoDB](https://img.shields.io/badge/MongoDB-191f32?style=for-the-badge&logo=mongodb&logoColor=47A248)
![Python](https://img.shields.io/badge/Python-191f32?style=for-the-badge&logo=python&logoColor=3776AB)
![FastAPI](https://img.shields.io/badge/FastAPI-191f32?style=for-the-badge&logo=fastapi&logoColor=009688)
![Flask](https://img.shields.io/badge/Flask-191f32?style=for-the-badge&logo=flask&logoColor=ffffff)
![OpenCV](https://img.shields.io/badge/OpenCV-191f32?style=for-the-badge&logo=opencv&logoColor=5C3EE8)

**Embedded Systems & Connected Hardware**

![Arduino](https://img.shields.io/badge/Arduino-191f32?style=for-the-badge&logo=arduino&logoColor=00979D)
![ESP32](https://img.shields.io/badge/ESP32_%2F_ESP32--S3-191f32?style=for-the-badge&logo=espressif&logoColor=E7352C)
![C++](https://img.shields.io/badge/C%2B%2B-191f32?style=for-the-badge&logo=cplusplus&logoColor=00599C)
![Bluetooth](https://img.shields.io/badge/BLE-191f32?style=for-the-badge&logo=bluetooth&logoColor=0082FC)
![IoT](https://img.shields.io/badge/IoT-191f32?style=for-the-badge&logo=internetofthings&logoColor=ffffff)
![RFID](https://img.shields.io/badge/RFID-191f32?style=for-the-badge&logoColor=ffffff)
![SPI](https://img.shields.io/badge/SPI_%7C_I2C_%7C_UART-191f32?style=for-the-badge&logoColor=ffffff)

**Engineering & Delivery**

![Git](https://img.shields.io/badge/Git-191f32?style=for-the-badge&logo=git&logoColor=F05032)
![GitHub](https://img.shields.io/badge/GitHub-191f32?style=for-the-badge&logo=github&logoColor=ffffff)
![REST APIs](https://img.shields.io/badge/REST_APIs-191f32?style=for-the-badge&logoColor=ffffff)
![JWT](https://img.shields.io/badge/JWT-191f32?style=for-the-badge&logo=jsonwebtokens&logoColor=ffffff)
![Vercel](https://img.shields.io/badge/Vercel-191f32?style=for-the-badge&logo=vercel&logoColor=ffffff)
![Render](https://img.shields.io/badge/Render-191f32?style=for-the-badge&logo=render&logoColor=46E3B7)

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

## 🚀 Other Projects

| Project | Focus | Link |
| --- | --- | --- |
| **Money-Mediia** | MERN-based employee management, payroll/leave features, and authentication | [Repository](https://github.com/FinancialNoobster/Money-Mediia) |
| **MAD 2 – Placement Portal** | Placement application, Vue frontend, and backend workflows | [Repository](https://github.com/FinancialNoobster/Mad_2_Placement-Portal-Application) |
| **MAD 1 – Placement Portal** | Placement-management application | [Repository](https://github.com/FinancialNoobster/Mad_1_Placement-Portal-Application) |
| **Backend Hardware Testing** | Experiments connecting backend services with physical devices | [Repository](https://github.com/FinancialNoobster/Backend-Hardware-Testing) |

---

## 📊 GitHub Statistics

<div align="center">

![GitHub stats](https://github-readme-stats.vercel.app/api?username=FinancialNoobster&show_icons=true&theme=tokyonight&hide_border=true&include_all_commits=true&rank_icon=github)
![Top repository languages](https://github-readme-stats.vercel.app/api/top-langs/?username=FinancialNoobster&layout=compact&theme=tokyonight&hide_border=true&langs_count=8)

![GitHub streak](https://streak-stats.demolab.com?user=FinancialNoobster&theme=tokyonight&hide_border=true)

</div>

## 🏆 GitHub Trophies

<div align="center">

![GitHub trophies](https://github-profile-trophy.vercel.app/?username=FinancialNoobster&theme=tokyonight&no-frame=true&no-bg=true&column=5&margin-w=8&margin-h=8)

</div>

## 📈 Contribution Activity

![Contribution graph](https://github-readme-activity-graph.vercel.app/graph?username=FinancialNoobster&theme=tokyo-night&hide_border=true&area=true)

## 🤝 Connect

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-FinancialNoobster-171e33?style=for-the-badge&logo=github)](https://github.com/FinancialNoobster)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Viranch_Gupta-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/viranch-gupta-99667b18b)

**Building products that connect people, software, and hardware.** ⚡

</div>

<!-- Dynamic stats, streaks, and trophies are provided by third-party services and may occasionally be unavailable. -->
