# 🔍 SubX Recon Scanner

SubX Recon Scanner is a fast and modern reconnaissance tool built for bug bounty hunters and penetration testers.

It automates the entire subdomain reconnaissance workflow by integrating multiple industry-standard tools into a simple graphical interface.

Instead of running several commands manually, SubX performs everything from one click and produces a professional HTML report.

---

## ✨ Features

- GUI built with CustomTkinter
- Passive Subdomain Enumeration
- Uses Subfinder
- Uses Amass
- Live Host Detection using httpx
- Progress Bar
- Scan Timer
- Real-time Scan Logs
- Automatic HTML Report Generation
- Dark Modern Dashboard
- Active & Inactive Host Separation
- Clickable URLs in Reports
- One-click Scan

---

## 📷 Preview

(Add screenshots here)

---

## 🛠 Tech Stack

- Python 3
- CustomTkinter
- Subfinder
- Amass
- httpx
- HTML
- TailwindCSS

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/subscanx.git
```

Go into the folder

```bash
cd subscanx
```

Install Python dependencies

```bash
pip install customtkinter
```

Install Recon Tools

### Subfinder

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### Httpx

```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### Amass

Install according to your operating system.

---

## Usage

Run

```bash
python subscanx.py
```

Enter the target domain

Example

```
example.com
```

Choose where to save the report.

Click **Start Scan**.

The tool will:

- Enumerate subdomains
- Validate live hosts
- Separate active and inactive targets
- Generate a responsive HTML report

---

## Generated Report

The report contains:

- Total Subdomains
- Active Hosts
- Inactive Hosts
- Clickable URLs
- Professional Dashboard
- Dark Theme

---

## Intended Users

- Bug Bounty Hunters
- Penetration Testers
- Red Teamers
- Security Researchers
- Students Learning Recon

---

## Disclaimer

This tool is intended for educational purposes and authorized security testing only. Do not scan systems without proper permission.

---

## License

MIT License
