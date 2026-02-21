import subprocess
from dataclasses import dataclass

@dataclass
class CmdResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str

def run(cmd: list[str], timeout: int = 30) -> CmdResult:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return CmdResult(
        ok=(p.returncode == 0),
        returncode=p.returncode,
        stdout=(p.stdout or "").strip(),
        stderr=(p.stderr or "").strip(),
    )

def is_active(service_name="jboss") -> bool:
    r = run(["systemctl", "is-active", service_name], timeout=10)
    return r.ok and r.stdout == "active"

def status(service_name="jboss") -> CmdResult:
    return run(["systemctl", "status", service_name, "--no-pager"], timeout=20)

def start(service_name="jboss") -> CmdResult:
    return run(["sudo", "systemctl", "start", service_name], timeout=90)
