import re
import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse
import requests
from PIL import Image, ImageTk
import cv2
import io
import os
import time

# -----------------------------
# URL ANALYZER (heuristic + network)
# -----------------------------
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "bank",
    "reset", "gift", "free", "winning", "confirm", "otp", "password"
]
SUSPICIOUS_TLDS = ["zip", "xyz", "top", "info", "cn", "ru", "rest", "gq", "tk"]

def is_ip(host):
    return bool(re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", host or ""))

def analyze_url(url):
    details = []
    score = 0

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url  # allow raw domains pasted in

    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = (parsed.path or "") + ("?" + parsed.query if parsed.query else "")

        # 1) Scheme (http vs https)
        if parsed.scheme.lower() != "https":
            score += 2
            details.append("Uses HTTP instead of HTTPS (+2)")

        # 2) IP address instead of domain
        if is_ip(host):
            score += 3
            details.append("IP address used as host (+3)")

        # 3) Too many dots in host
        dot_count = host.count(".")
        if dot_count >= 3:
            score += 1
            details.append(f"Unusually deep subdomain ({dot_count} dots) (+1)")

        # 4) Hyphen in domain (often used for lookalikes)
        if "-" in host:
            score += 1
            details.append("Hyphen in domain (+1)")

        # 5) '@' in URL (redirect trick)
        if "@" in url:
            score += 3
            details.append("Contains '@' (redirect obfuscation) (+3)")

        # 6) Suspicious TLD
        tld = host.split(".")[-1].lower() if "." in host else ""
        if tld in SUSPICIOUS_TLDS:
            score += 1
            details.append(f"Suspicious TLD .{tld} (+1)")

        # 7) Length
        length = len(url)
        if length > 120:
            score += 2
            details.append(f"Very long URL ({length} chars) (+2)")
        elif length > 75:
            score += 1
            details.append(f"Long URL ({length} chars) (+1)")

        # 8) Encoded/param heavy
        special = url.count("%") + url.count("=") + url.count("&") + url.count("?")
        if special >= 6:
            score += 1
            details.append("Heavily parameterized/encoded (+1)")

        # 9) Phishing keywords
        low_url = url.lower()
        hit_words = [w for w in SUSPICIOUS_KEYWORDS if w in low_url]
        if hit_words:
            score += 2
            details.append(f"Phish-like keywords: {', '.join(hit_words)} (+2)")

        # 10) Simple network reachability (optional signal)
        reachable = False
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Student Project)"}
            r = requests.head(url, allow_redirects=True, timeout=5, headers=headers)
            if r.status_code >= 200 and r.status_code < 400:
                reachable = True
        except:
            pass

        if not reachable:
            # Try GET lightly (some hosts block HEAD)
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Student Project)"}
                r = requests.get(url, allow_redirects=True, timeout=6, headers=headers)
                if r.status_code >= 200 and r.status_code < 400:
                    reachable = True
            except:
                pass

        if not reachable:
            details.append("Not reachable or blocked by server (0)")
            # note: not increasing score; unreachable could be temporary

        # Decision
        if score >= 6:
            verdict = "HIGH RISK"
        elif score >= 3:
            verdict = "SUSPICIOUS"
        else:
            verdict = "LOW RISK"

        return {
            "input": url,
            "host": host,
            "scheme": parsed.scheme,
            "score": score,
            "verdict": verdict,
            "details": details,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        return {
            "input": url,
            "error": str(e),
            "verdict": "INVALID URL",
            "details": ["Could not parse/analyze the URL."],
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

# -----------------------------
# QR DECODER (OpenCV)
# -----------------------------
def decode_qr(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, "Could not read image."
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    if data:
        return data, None
    return None, "No QR code found in the image."

# -----------------------------
# GUI
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fake QR & Phishing URL Detector")
        self.geometry("720x560")
        self.minsize(720, 560)

        # Title
        tk.Label(self, text="Fake QR & Phishing URL Detector", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # URL Frame
        url_frame = tk.LabelFrame(self, text="Check URL", padx=10, pady=10)
        url_frame.pack(fill="x", padx=12, pady=8)

        self.url_var = tk.StringVar()
        tk.Entry(url_frame, textvariable=self.url_var, font=("Segoe UI", 11)).pack(side="left", fill="x", expand=True)
        tk.Button(url_frame, text="Analyze", command=self.on_analyze_url).pack(side="left", padx=8)

        # QR Frame
        qr_frame = tk.LabelFrame(self, text="Scan QR Image", padx=10, pady=10)
        qr_frame.pack(fill="x", padx=12, pady=8)

        tk.Button(qr_frame, text="Upload QR Image", command=self.on_upload_qr).pack(side="left")
        self.qr_preview = tk.Label(qr_frame)
        self.qr_preview.pack(side="left", padx=12)

        # Results
        res_frame = tk.LabelFrame(self, text="Result", padx=10, pady=10)
        res_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.verdict_lbl = tk.Label(res_frame, text="Verdict: —", font=("Segoe UI", 13, "bold"))
        self.verdict_lbl.pack(anchor="w")

        self.details_txt = tk.Text(res_frame, height=12, wrap="word")
        self.details_txt.pack(fill="both", expand=True, pady=6)

        # Footer buttons
        footer = tk.Frame(self)
        footer.pack(fill="x", padx=12, pady=8)

        tk.Button(footer, text="Export Report", command=self.on_export).pack(side="left")
        tk.Button(footer, text="Clear", command=self.on_clear).pack(side="left", padx=8)
        tk.Button(footer, text="Exit", command=self.quit).pack(side="right")

        self.last_result = None
        self.last_image_tk = None

    def on_analyze_url(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Input needed", "Please enter a URL.")
            return
        result = analyze_url(url)
        self.show_result(result)

    def on_upload_qr(self):
        path = filedialog.askopenfilename(
            title="Select QR Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if not path:
            return

        # preview
        try:
            img = Image.open(path)
            img.thumbnail((160, 160))
            self.last_image_tk = ImageTk.PhotoImage(img)
            self.qr_preview.configure(image=self.last_image_tk)
        except:
            self.qr_preview.configure(image="")

        # decode
        data, err = decode_qr(path)
        if err:
            messagebox.showwarning("QR Scan", err)
            return
        self.url_var.set(data)
        result = analyze_url(data)
        self.show_result(result)

    def show_result(self, result):
        self.last_result = result
        self.details_txt.delete("1.0", "end")

        if "error" in result and result["verdict"] == "INVALID URL":
            self.verdict_lbl.config(text=f"Verdict: INVALID URL")
            self.details_txt.insert("end", f"Error: {result['error']}\n")
            for d in result["details"]:
                self.details_txt.insert("end", f"- {d}\n")
            return

        self.verdict_lbl.config(text=f"Verdict: {result['verdict']} (score {result['score']})")
        info_lines = [
            f"Checked: {result['input']}",
            f"Host:    {result.get('host','—')}",
            f"Time:    {result['time']}",
            "",
            "Signals:"
        ]
        for line in info_lines:
            self.details_txt.insert("end", line + "\n")
        if result["details"]:
            for d in result["details"]:
                self.details_txt.insert("end", f"• {d}\n")

    def on_export(self):
        if not self.last_result:
            messagebox.showinfo("Export Report", "Nothing to export yet.")
            return
        default_name = f"report_{int(time.time())}.txt"
        path = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text Files", "*.txt")]
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            r = self.last_result
            f.write("Fake QR & Phishing URL Detector Report\n")
            f.write("="*42 + "\n\n")
            f.write(f"Time:    {r['time']}\n")
            f.write(f"Input:   {r['input']}\n")
            f.write(f"Host:    {r.get('host','—')}\n")
            f.write(f"Verdict: {r['verdict']} (score {r.get('score','—')})\n\n")
            if r.get("details"):
                f.write("Signals:\n")
                for d in r["details"]:
                    f.write(f"- {d}\n")
        messagebox.showinfo("Export Report", f"Saved: {os.path.basename(path)}")

    def on_clear(self):
        self.url_var.set("")
        self.qr_preview.configure(image="")
        self.verdict_lbl.config(text="Verdict: —")
        self.details_txt.delete("1.0", "end")
        self.last_result = None

if __name__ == "__main__":
    App().mainloop()