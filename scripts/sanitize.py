#!/usr/bin/env python3
"""
Scrub production identifiers out of the demo artifacts before publishing them.

The diagrams in docs/demos/ were generated live against a real AWS account. Their
shapes and findings are the point of the talk; the account number is not. This
rewrites every identifier to a deterministic, obviously-fake stand-in so the
published HTML stays structurally identical to what ran on stage.

Deterministic on purpose: a given real ID always maps to the same fake ID, within
and across files, so the cross-references in the diagrams still line up.

Nothing sensitive lives in this file. The two values that *are* sensitive -- the
account number and the internal org/environment token -- are supplied at runtime
and never committed:

    export SANITIZE_ACCOUNT=<real 12-digit account id>
    export SANITIZE_ORG=<real org token appearing in names and DNS>

    python3 scripts/sanitize.py IN.html OUT.html [IN2.html OUT2.html ...]
    python3 scripts/sanitize.py --check FILE.html ...

--check is safe to run in CI without the env vars: it verifies the generic
markers (routable IPs, real-looking IPv6, hosted zone IDs). Supply the env vars
to additionally assert the account number and org token are absent.

Reserved ranges used for replacements:
    RFC 5737  203.0.113.0/24            IPv4 documentation
    RFC 3849  2001:db8::/32             IPv6 documentation
    AWS docs  123456789012              account ID
"""

import hashlib
import os
import re
import sys

FAKE_ACCOUNT = "123456789012"
FAKE_ORG = "acme"

# Secondary environment tokens: short, ambiguous strings that need anchored
# patterns rather than a blind replace. Supplied as  real:fake  pairs.
EXTRA_TOKENS = os.environ.get("SANITIZE_EXTRA", "")

# AWS resource ID prefixes followed by lowercase hex.
HEX_ID = re.compile(
    r"\b(vpc|subnet|sg|sgr|eni|i|vol|ami|igw|eigw|nat|rtb|acl|vpce|pl|lb|tg)-([0-9a-f]{8,17})\b"
)
# Cloud Map namespace IDs.
NS_ID = re.compile(r"\bns-([a-z0-9]{10,32})\b")
# Route 53 hosted zone IDs.
ZONE_ID = re.compile(r"\bZ[A-Z0-9]{9,31}\b")
IPV4 = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")

# IPv6 in every form these artifacts use:
#   full            2a0f:c0de:1111:2200:aaaa:bbbb:cccc:dddd
#   compressed net  2a0f:c0de:1111:2200::/56
#   abbreviated     ...aaaa:bbbb:cccc:dddd   (interface identifier only)
# Requires at least three colons, so wall-clock times like 17:12:37 never match.
IPV6 = re.compile(
    r"(?<![0-9a-fA-F:])"
    r"(?:[0-9a-fA-F]{1,4}:){3,7}(?:[0-9a-fA-F]{1,4})?:?"
    r"(?![0-9a-fA-F])"
)

# Internal addressing, remapped wholesale so every /18 and /20 relationship in
# the diagrams survives intact.
INTERNAL_FROM = ("172", "24")
INTERNAL_TO = ("10", "20")


def _digest(value: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{value}".encode()).hexdigest()


def _is_reserved_v4(o) -> bool:
    """True for addresses that are already private, loopback, or documentation."""
    return (
        o[0] in (0, 10, 127)
        or (o[0] == 169 and o[1] == 254)
        or (o[0] == 172 and 16 <= o[1] <= 31)
        or (o[0] == 192 and o[1] == 168)
        or (o[0] == 192 and o[1] == 0 and o[2] == 2)
        or (o[0] == 198 and o[1] == 51 and o[2] == 100)
        or (o[0] == 203 and o[1] == 0 and o[2] == 113)
        or o[0] >= 224
    )


class Sanitizer:
    def __init__(self, account=None, org=None, extra=""):
        self.account = account
        self.org = org
        self.extra = []
        for pair in filter(None, (p.strip() for p in extra.split(","))):
            real, _, fake = pair.partition(":")
            if real and fake:
                self.extra.append((real, fake))
        self.public_v4 = {}
        self.v6 = {}
        self.hits = {}

    def _note(self, kind, n=1):
        self.hits[kind] = self.hits.get(kind, 0) + n

    def _hex_id(self, m):
        prefix, body = m.group(1), m.group(2)
        self._note(f"{prefix}-*")
        # Preserve prefix and total length; real AWS IDs lead with 0.
        return f"{prefix}-0{_digest(m.group(0), 'hexid')[: len(body) - 1]}"

    def _ns_id(self, m):
        self._note("ns-*")
        return "ns-" + _digest(m.group(0), "nsid")[: len(m.group(1))]

    def _zone_id(self, m):
        tok = m.group(0)
        self._note("hosted zone ID")
        return "Z" + _digest(tok, "zone")[: len(tok) - 1].upper()

    def _ipv4(self, m):
        octets = [m.group(i) for i in range(1, 5)]
        if any(int(x) > 255 for x in octets):
            return m.group(0)
        if (octets[0], octets[1]) == INTERNAL_FROM:
            self._note("internal IPv4")
            return ".".join(INTERNAL_TO + tuple(octets[2:]))
        if _is_reserved_v4([int(x) for x in octets]):
            return m.group(0)
        key = m.group(0)
        if key not in self.public_v4:
            self.public_v4[key] = f"203.0.113.{10 + len(self.public_v4)}"
        self._note("routable IPv4")
        return self.public_v4[key]

    def _ipv6(self, m):
        tok = m.group(0)
        low = tok.lower()
        if low.startswith("2001:db8"):
            return tok
        d = _digest(low.rstrip(":"), "v6")

        # Network prefix such as 2a0f:c0de:1111:2200::/56 -- keep it a prefix.
        if tok.endswith("::"):
            self._note("IPv6 prefix")
            return f"2001:db8:{d[0:4]}:{d[4:8]}::"

        groups = [g for g in low.split(":") if g]
        if len(groups) >= 8:
            self._note("IPv6 address")
            return "2001:db8:" + ":".join(d[i : i + 4] for i in range(0, 24, 4))

        # Abbreviated interface identifier: keep the same number of groups so the
        # diagram's column alignment is unchanged. Lead with "db8" so the value is
        # recognisable as documentation data even with no prefix attached.
        self._note("IPv6 fragment")
        n = len(groups)
        out = ":".join(["db8"] + [d[i : i + 4] for i in range(0, 4 * (n - 1), 4)])
        return out + ":" if tok.endswith(":") else out

    def run(self, text):
        if self.org:
            text, n = re.subn(re.escape(self.org), FAKE_ORG, text, flags=re.I)
            if n:
                self._note("org token", n)
        for real, fake in self.extra:
            text, n = re.subn(re.escape(real), fake, text)
            if n:
                self._note(f"extra token {real!r}", n)
        if self.account:
            text, n = re.subn(re.escape(self.account), FAKE_ACCOUNT, text)
            if n:
                self._note("account ID", n)

        text = IPV6.sub(self._ipv6, text)
        text = ZONE_ID.sub(self._zone_id, text)
        text = NS_ID.sub(self._ns_id, text)
        text = HEX_ID.sub(self._hex_id, text)
        text = IPV4.sub(self._ipv4, text)
        return text

    def report(self):
        if not self.hits:
            return "  nothing matched"
        w = max(len(k) for k in self.hits)
        return "\n".join(f"  {k:<{w}}  {v}" for k, v in sorted(self.hits.items()))


def audit(text, account=None, org=None):
    """Report anything that still looks like production data.

    Resource IDs are deliberately not shape-checked: every ID is rewritten
    unconditionally, so a sanitized ID and a real one are indistinguishable by
    shape. The decisive signals are the account number, the org token, routable
    addresses, and hosted zone IDs outside the generated form.
    """
    findings = []
    if account and account in text:
        findings.append(f"account ID {account}")
    if org and re.search(re.escape(org), text, re.I):
        findings.append(f"org token {org!r}")

    for m in IPV6.finditer(text):
        tok = m.group(0)
        low = tok.lower()
        # 2001:db8::/32 is the documentation prefix; a leading "db8" group marks an
        # abbreviated interface identifier that this script generated.
        if low.startswith("2001:db8") or low.startswith("db8:"):
            continue
        findings.append(f"non-documentation IPv6 {tok}")

    for m in IPV4.finditer(text):
        o = [int(x) for x in m.groups()]
        if any(x > 255 for x in o) or _is_reserved_v4(o):
            continue
        findings.append(f"routable IPv4 {m.group(0)}")

    return findings


def main(argv):
    account = os.environ.get("SANITIZE_ACCOUNT") or None
    org = os.environ.get("SANITIZE_ORG") or None

    if argv and argv[0] == "--check":
        paths = argv[1:]
        if not paths:
            print("--check needs at least one file", file=sys.stderr)
            return 2
        bad = False
        for path in paths:
            with open(path, encoding="utf-8") as fh:
                findings = audit(fh.read(), account, org)
            if findings:
                bad = True
                print(f"FAIL {path}")
                for f in sorted(set(findings)):
                    print(f"  leaked: {f}")
            else:
                print(f"OK   {path}")
        if not (account and org):
            print("note: SANITIZE_ACCOUNT / SANITIZE_ORG unset -- generic checks only")
        return 1 if bad else 0

    if not argv or len(argv) % 2:
        print(__doc__)
        return 2
    if not (account and org):
        print(
            "refusing to run: set SANITIZE_ACCOUNT and SANITIZE_ORG first",
            file=sys.stderr,
        )
        return 2

    for src, dst in zip(argv[::2], argv[1::2]):
        with open(src, encoding="utf-8") as fh:
            original = fh.read()
        s = Sanitizer(account, org, EXTRA_TOKENS)
        cleaned = s.run(original)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(cleaned)
        print(f"{src}\n  -> {dst}")
        print(s.report())
        remaining = audit(cleaned, account, org)
        if remaining:
            print("  STILL DIRTY:")
            for f in sorted(set(remaining)):
                print(f"    {f}")
            return 1
        print("  audit: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
