# python/resonance_dn/dn.py
from __future__ import annotations
import hashlib
import urllib.parse
from dataclasses import dataclass
from typing import Any, List, Optional, Union, Dict

DN = str
DNPart = Union[str, Dict[str, Any]]

@dataclass
class DNOptions:
    scheme: str = ""
    normalize_case: bool = True
    max_part_len: int = 256

class DNBuilder:
    def __init__(self, opts: Optional[DNOptions] = None) -> None:
        self.opts = opts or DNOptions()

    def build(self, parts: List[DNPart], prefix: Optional[DN] = None) -> DN:
        segs: List[str] = []
        if self.opts.scheme:
            segs.append(f"{self.opts.scheme}://")
        if prefix:
            segs.append(self.strip_scheme(prefix).rstrip("/"))

        for p in parts:
            if isinstance(p, str):
                seg = self._encode_segment(p)
            else:
                k = p.get("k", "")
                v = p.get("v", None)
                seg = self._encode_kv(k, v)
            if seg:
                segs.append(seg)

        out = "/".join([s for s in segs if s]).replace("//", "/")
        scheme_token = f"{self.opts.scheme}://"
        if self.opts.scheme and out.startswith(scheme_token):
            return out
        return out.lstrip("/")

    def parent(self, dn: DN) -> DN:
        raw = self.strip_scheme(dn).rstrip("/")
        idx = raw.rfind("/")
        if idx <= 0:
            return self.restore_scheme(dn, raw)
        return self.restore_scheme(dn, raw[:idx])

    def split(self, dn: DN) -> List[str]:
        raw = self.strip_scheme(dn).rstrip("/")
        return [p for p in raw.split("/") if p]

    def prefix(self, dn: DN, depth: int) -> DN:
        parts = self.split(dn)
        raw = "/".join(parts[: max(0, depth)])
        return self.restore_scheme(dn, raw)

    def hash(self, dn: DN, bytes_: int = 8) -> str:
        h = hashlib.sha256(dn.encode("utf-8")).hexdigest()
        return h[: bytes_ * 2]

    def strip_scheme(self, dn: DN) -> str:
        if not self.opts.scheme:
            return dn
        token = f"{self.opts.scheme}://"
        return dn[len(token):] if dn.startswith(token) else dn

    def restore_scheme(self, original: DN, raw: str) -> DN:
        if not self.opts.scheme:
            return raw
        token = f"{self.opts.scheme}://"
        return f"{token}{raw}" if original.startswith(token) else raw

    def _encode_kv(self, k: str, v: Any) -> str:
        kk = self._encode_segment(k)
        if v is None:
            return kk
        vv = self._encode_segment(str(v))
        return f"{kk}:{vv}"

    def _encode_segment(self, s: str) -> str:
        x = s.strip()
        if not x:
            return ""
        if self.opts.normalize_case:
            x = x # Add NFKC normalization if needed
        x = urllib.parse.quote(x, safe="")
        x = x.replace("%2F", "_").replace("%3A", "~")
        if len(x) > self.opts.max_part_len:
            x = x[: self.opts.max_part_len]
        return x