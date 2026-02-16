from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    risk_score = 0
    reasons = []

    # Check HTTPS
    if not url.startswith("https"):
        risk_score += 2
        reasons.append("Not using HTTPS")

    # Check URL length
    if len(url) > 30:
        risk_score += 1
        reasons.append("URL is unusually long")

    # Suspicious keywords
    suspicious_words = ["login", "verify", "update", "bank", "secure", "account"]
    for word in suspicious_words:
        if word in url.lower():
            risk_score += 2
            reasons.append(f"Contains suspicious word: {word}")

    # IP address check
    if re.match(r"^http[s]?://\d+\.\d+\.\d+\.\d+", url):
        risk_score += 3
        reasons.append("Uses IP address instead of domain")

    # Final result
    if risk_score >= 4:
        result = "⚠ HIGH RISK: Possible Phishing Website"
    elif risk_score >= 2:
        result = "⚠ MEDIUM RISK: Suspicious Website"
    else:
        result = "✅ SAFE Website"

    return render_template("result.html", result=result, reasons=reasons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


