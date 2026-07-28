#!/usr/bin/env python3
"""Wrap a rendered HTML deck in a client-side AES-256-GCM password gate.

PBKDF2-HMAC-SHA256 (250k iterations) derives the key from the password; the whole
document is encrypted and only decrypted in the browser via WebCrypto. The
plaintext never ships. Styling follows the Astfalck design system.
"""
import base64
import json
import os
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib

ITERATIONS = 250_000

GATE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE__</title>
<style>
@font-face { font-family:"Clancy"; src:url("../../fonts/Clancy-Regular.otf") format("opentype"); font-weight:400; font-display:swap; }
@font-face { font-family:"Clancy"; src:url("../../fonts/Clancy-Bold.otf") format("opentype"); font-weight:600 700; font-display:swap; }
@font-face { font-family:"Roboto"; src:url("../../fonts/Roboto-Regular.ttf") format("truetype"); font-weight:400; font-display:swap; }
@font-face { font-family:"Roboto Mono"; src:url("../../fonts/RobotoMono-Regular.ttf") format("truetype"); font-weight:400; font-display:swap; }
:root {
  --paper: #F8F7F3; --paper-sunk: #EEEBE3; --surface: #FCFBF9;
  --ink: #211C16; --ink-2: #4A4239; --ink-3: #8A8073;
  --line: rgba(33, 28, 22, 0.12);
  --sage: #5A7468; --sage-deep: #41564C; --terracotta: #9D5242; --yellow: #FFDC00;
}
* { box-sizing: border-box; }
html, body { height: 100%; }
body {
  margin: 0; background: var(--paper); color: var(--ink);
  font-family: "Roboto", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 18px; line-height: 1.65;
  display: flex; align-items: center; justify-content: center; padding: 2rem;
}
.gate { width: 100%; max-width: 30rem; }
.kicker {
  font-family: "Roboto Mono", ui-monospace, Menlo, monospace;
  font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-3); margin: 0 0 0.75rem;
}
h1 {
  font-family: "Clancy", "Roboto", sans-serif; font-weight: 600;
  font-size: 1.75rem; line-height: 1.25; margin: 0 0 0.5rem;
}
.rule { height: 2px; width: 3rem; background: var(--yellow); margin: 1.25rem 0; }
p.note { color: var(--ink-2); font-size: 0.95rem; margin: 0 0 1.5rem; }
form { display: flex; gap: 0.5rem; }
input[type="password"] {
  flex: 1; font: inherit; font-size: 1rem; color: var(--ink);
  background: var(--surface); border: 1px solid var(--line); border-radius: 4px;
  padding: 0.6rem 0.75rem; transition: border-color 200ms;
}
input[type="password"]:focus { outline: none; border-color: var(--sage); }
button {
  font: inherit; font-size: 1rem; color: var(--paper); background: var(--sage-deep);
  border: none; border-radius: 4px; padding: 0.6rem 1.25rem; cursor: pointer;
  transition: background 200ms;
}
button:hover { background: var(--terracotta); }
button:disabled { opacity: 0.6; cursor: default; }
.msg { min-height: 1.5rem; margin: 0.75rem 0 0; font-size: 0.9rem; color: var(--terracotta); }
.back {
  display: inline-block; margin-top: 2rem; font-size: 0.9rem;
  color: var(--sage-deep); text-decoration: none;
}
.back:hover { color: var(--terracotta); }
</style>
</head>
<body>
<div class="gate">
  <p class="kicker">Protected slides</p>
  <h1>__TITLE__</h1>
  <div class="rule"></div>
  <p class="note">These slides are password protected. Enter the password to view them.</p>
  <form id="f" autocomplete="off">
    <input type="password" id="pw" placeholder="Password" aria-label="Password" autofocus>
    <button type="submit" id="go">Open</button>
  </form>
  <p class="msg" id="msg" role="status"></p>
  <a class="back" href="../../presentations.html">&larr; All presentations</a>
</div>
<script id="payload" type="application/json">__PAYLOAD__</script>
<script>
(function () {
  var data = JSON.parse(document.getElementById("payload").textContent);
  var msg = document.getElementById("msg");
  var btn = document.getElementById("go");

  function b64(s) {
    var bin = atob(s), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  if (!window.crypto || !window.crypto.subtle) {
    msg.textContent = "This page needs a secure (https) connection to decrypt.";
    btn.disabled = true;
    return;
  }

  document.getElementById("f").addEventListener("submit", function (e) {
    e.preventDefault();
    var pw = document.getElementById("pw").value;
    if (!pw) return;
    msg.style.color = "var(--ink-3)";
    msg.textContent = "Decrypting\\u2026";
    btn.disabled = true;

    crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: "PBKDF2", salt: b64(data.salt), iterations: data.iterations, hash: "SHA-256" },
          base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
      })
      .then(function (key) {
        return crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(data.iv) }, key, b64(data.ct));
      })
      .then(function (plain) {
        var html = new TextDecoder().decode(plain);
        document.open();
        document.write(html);
        document.close();
      })
      .catch(function () {
        msg.style.color = "var(--terracotta)";
        msg.textContent = "Wrong password.";
        btn.disabled = false;
        document.getElementById("pw").select();
      });
  });
})();
</script>
</body>
</html>
"""


def main():
    src, dest, password, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    plaintext = open(src, "rb").read()
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS, dklen=32)
    ct = AESGCM(key).encrypt(iv, plaintext, None)

    payload = json.dumps({
        "salt": base64.b64encode(salt).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ct": base64.b64encode(ct).decode(),
        "iterations": ITERATIONS,
    })

    html = (GATE_TEMPLATE
            .replace("__PAYLOAD__", payload)
            .replace("__TITLE__", title))
    open(dest, "w").write(html)

    # Verify the round trip before declaring success.
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS, dklen=32)
    assert AESGCM(check).decrypt(iv, ct, None) == plaintext, "round-trip failed"

    print("plaintext  %8d bytes  %s" % (len(plaintext), src))
    print("gate page  %8d bytes  %s" % (os.path.getsize(dest), dest))
    print("round-trip decrypt OK")


if __name__ == "__main__":
    main()
