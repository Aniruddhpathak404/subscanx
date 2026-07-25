import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading, subprocess, webbrowser, os, time

SUBFINDER = "/home/aniruddh/go/bin/subfinder"
AMASS = "/usr/lib/amass/amass"
HTTPX = "/home/aniruddh/go/bin/httpx"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ReconTool:
    def __init__(self, root):
        self.root = root
        self.root.title("SubX Recon Scanner")
        self.root.geometry("1000x700")
        self.save_path = ""
        self.start_time = None
        self.scanning = False

        ctk.CTkLabel(root, text="SubX Recon Scanner", font=("Segoe UI", 28, "bold")).pack(pady=15)

        self.domain_entry = ctk.CTkEntry(root, width=500, placeholder_text="example.com")
        self.domain_entry.pack(pady=10)

        ctk.CTkButton(root, text="Choose Report Location", command=self.choose_report).pack(pady=5)
        self.path_label = ctk.CTkLabel(root, text="No report selected")
        self.path_label.pack()

        ctk.CTkButton(root, text="Start Scan", command=self.start_scan).pack(pady=10)

        self.progress = ctk.CTkProgressBar(root, width=700)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.percent_label = ctk.CTkLabel(root, text="Progress: 0%")
        self.percent_label.pack()

        self.time_label = ctk.CTkLabel(root, text="Elapsed: 00:00:00")
        self.time_label.pack()

        self.stats = ctk.CTkLabel(root, text="Total: 0 | Active: 0 | Inactive: 0")
        self.stats.pack(pady=10)

        self.logs = ctk.CTkTextbox(root, width=900, height=400)
        self.logs.pack(padx=10, pady=10, fill="both", expand=True)

    def choose_report(self):
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if path:
            self.save_path = path
            self.path_label.configure(text=path)

    def log(self, msg):
        self.logs.insert("end", msg + "\n")
        self.logs.see("end")

    def update_progress(self, val, msg=""):
        self.progress.set(val)
        self.percent_label.configure(text=f"Progress: {int(val * 100)}% {msg}")

    def update_timer(self):
        if self.scanning:
            e = int(time.time() - self.start_time)
            self.time_label.configure(text=f"Elapsed: {e // 3600:02}:{(e % 3600) // 60:02}:{e % 60:02}")
            self.root.after(1000, self.update_timer)

    def start_scan(self):
        if not self.domain_entry.get().strip():
            messagebox.showerror("Error", "Enter a domain")
            return
        if not self.save_path:
            messagebox.showerror("Error", "Choose report location first")
            return
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        domain = self.domain_entry.get().strip()
        self.start_time = time.time()
        self.scanning = True
        self.root.after(0, self.update_timer)

        try:
            self.update_progress(0.05, "Checking tools")

            for tool in [SUBFINDER, AMASS, HTTPX]:
                if not os.path.exists(tool):
                    self.log(f"[ERROR] Missing tool: {tool}")
                    return

            self.log("[+] Running Subfinder")
            try:
                subfinder = subprocess.check_output([SUBFINDER, "-d", domain, "-silent"], text=True, stderr=subprocess.DEVNULL).splitlines()
            except Exception as e:
                self.log(f"[!] Subfinder failed: {e}")
                subfinder = []

            self.update_progress(0.35, "Subfinder complete")

            self.log("[+] Running Amass")
            try:
                amass = subprocess.check_output([AMASS, "enum", "-passive", "-d", domain], text=True, stderr=subprocess.STDOUT, timeout=120).splitlines()
            except Exception as e:
                self.log(f"[!] Amass failed, continuing: {e}")
                amass = []

            self.update_progress(0.60, "Enumeration complete")

            all_subs = sorted(set(x.strip() for x in (subfinder + amass) if x.strip()))
            self.log(f"[+] Found {len(all_subs)} subdomains")

            if not all_subs:
                self.log("[!] No subdomains found")
                return

            temp = "/tmp/subx_subs.txt"
            with open(temp, "w") as f:
                f.write("\n".join(all_subs))

            self.log("[+] Checking active hosts")
            try:
                with open(temp, "r") as f:
                    active_raw = subprocess.check_output([HTTPX, "-silent"], stdin=f, text=True, stderr=subprocess.DEVNULL).splitlines()
                self.log(f"Raw HTTPX response preview: {len(active_raw)} entries found.")
            except Exception as e:
                self.log(f"[!] httpx failed: {e}")
                active_raw = []

            active_links = {}
            active_hosts = set()
            for line in active_raw:
                if not line.strip():
                    continue
                url = line.split()[0].strip()
                host = url.replace("https://", "").replace("http://", "").strip("/")
                active_hosts.add(host)
                active_links[host] = url

            inactive = [s for s in all_subs if s not in active_hosts]

            self.update_progress(0.90, "Generating report")

            # Beautiful, Responsive Tailwind CSS Dashboard template
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SubX Recon Report - {domain}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    </style>
</head>
<body class="p-8">
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-700 pb-6 mb-8">
            <div>
                <h1 class="text-4xl font-extrabold text-blue-400 tracking-tight">SubX Recon Scanner</h1>
                <p class="text-slate-400 mt-2 text-sm">Target Domain: <span class="text-slate-200 font-mono text-base">{domain}</span></p>
            </div>
            <div class="text-right text-xs text-slate-500">
                Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>

        <!-- Metric Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
                <div class="text-slate-400 font-medium uppercase tracking-wider text-xs">Total Subdomains</div>
                <div class="text-3xl font-bold mt-2 text-slate-100">{len(all_subs)}</div>
            </div>
            <div class="bg-emerald-950/40 p-6 rounded-xl border border-emerald-500/30 shadow-lg">
                <div class="text-emerald-400 font-medium uppercase tracking-wider text-xs">Active Targets</div>
                <div class="text-3xl font-bold mt-2 text-emerald-400">{len(active_hosts)}</div>
            </div>
            <div class="bg-rose-950/40 p-6 rounded-xl border border-rose-500/30 shadow-lg">
                <div class="text-rose-400 font-medium uppercase tracking-wider text-xs">Inactive Domains</div>
                <div class="text-3xl font-bold mt-2 text-rose-400">{len(inactive)}</div>
            </div>
        </div>

        <!-- Main Workspace Tables -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Active Section -->
            <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-xl">
                <h2 class="text-xl font-bold mb-4 text-emerald-400 flex items-center">
                    <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full inline-block mr-2 animate-pulse"></span>
                    Active Targets ({len(active_hosts)})
                </h2>
                <div class="overflow-y-auto max-h-[500px] pr-2">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-700 text-slate-400 text-sm">
                                <th class="pb-2 font-semibold">Subdomain Link</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-700/50">"""
            
            for s in sorted(active_hosts):
                link = active_links.get(s, f"http://{s}")
                html += f"""
                            <tr>
                                <td class="py-2.5 font-mono text-sm">
                                    <a href="{link}" target="_blank" class="text-blue-400 hover:text-blue-300 hover:underline transition flex items-center">
                                        {s}
                                        <svg class="w-3.5 h-3.5 ml-1.5 opacity-60" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                                    </a>
                                </td>
                            </tr>"""

            html += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Inactive Section -->
            <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-xl">
                <h2 class="text-xl font-bold mb-4 text-rose-400 flex items-center">
                    <span class="w-2.5 h-2.5 bg-rose-500 rounded-full inline-block mr-2"></span>
                    Inactive Domains ({len(inactive)})
                </h2>
                <div class="overflow-y-auto max-h-[500px] pr-2">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-700 text-slate-400 text-sm">
                                <th class="pb-2 font-semibold">Subdomain</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-700/50">"""

            for s in inactive:
                html += f"""
                            <tr>
                                <td class="py-2.5 font-mono text-sm text-slate-400 select-all">{s}</td>
                            </tr>"""

            html += """
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>
</body>
</html>"""

            with open(self.save_path, "w", encoding="utf-8") as f:
                f.write(html)

            self.stats.configure(text=f"Total: {len(all_subs)} | Active: {len(active_hosts)} | Inactive: {len(inactive)}")
            self.update_progress(1.0, "Finished")
            self.log(f"[+] Report saved: {self.save_path}")
            webbrowser.open("file://" + os.path.abspath(self.save_path))

        except Exception as e:
            self.log(f"[ERROR] {e}")
        finally:
            self.scanning = False

app = ctk.CTk()
ReconTool(app)
app.mainloop()
