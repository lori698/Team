"""PreToolUse guard for the Team agents.

Usage (hook command):  python -I C:/claude/Team/scripts/guard/team_guard.py --agent <name|auto>
Reads the hook JSON on stdin. Exit 0 = allow. Exit 2 = deny (message on stderr).

--agent <name>  : enforce that agent's profile (from policy.json). Fails CLOSED on any error.
--agent auto    : use payload agent_type if present, else treat as the owner's main session
                  (secrets and Team-folder checks only; git and deletes are handled by permission rules).
"""
import json
import os
import re
import shlex
import sys
import time
from fnmatch import fnmatch
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normcase(os.path.realpath(os.path.join(HERE, "..", "..")))
LOG = os.path.join(HERE, "guard_log.txt")
NAME_RE = re.compile(r"^[a-z0-9-]{1,40}$")

with open(os.path.join(HERE, "policy.json"), encoding="utf-8") as fh:
    POLICY = json.load(fh)


class Deny(Exception):
    pass


def norm(path, cwd):
    if not os.path.isabs(path):
        path = os.path.join(cwd or ROOT, path)
    return os.path.normcase(os.path.realpath(path))


def inside(path, root):
    root = os.path.normcase(os.path.realpath(root))
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:  # different drives
        return False


def log(agent, tool, decision, reason, target=""):
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (
                time.strftime("%Y-%m-%d %H:%M:%S"), agent, tool, decision, reason, str(target)[:160].replace("\n", " ")))
    except OSError:
        pass


def is_secret(text):
    low = text.lower()
    return any(re.search(p, low) for p in POLICY["secret_name_patterns"])


def profile_for(name):
    prof = dict(POLICY["default"])
    extra = POLICY["agents"].get(name, {})
    for k, v in extra.items():
        if k == "write_extra":
            continue
        prof[k] = v
    write = [r.replace("{name}", name) for r in prof["write"]]
    roots = [os.path.join(ROOT, w) for w in write]
    roots += extra.get("write_extra", [])
    return prof, roots


def check_write(path, name, cwd, roots):
    p = norm(path, cwd)
    if is_secret(p):
        raise Deny("secret-like path: " + p)
    parts = [x for x in re.split(r"[\\/]", p) if x]
    for part in parts:
        if part in POLICY["never_write_names"] or any(part.startswith(x) for x in POLICY["never_write_prefixes"]):
            raise Deny("protected folder or file name '%s' in %s" % (part, p))
    for prot in POLICY["team_protected"]:
        if inside(p, os.path.join(ROOT, prot)):
            raise Deny("Team-protected area (owner only): " + prot)
    if not any(inside(p, r) for r in roots):
        raise Deny("outside this agent's write boundary: " + p)


BAD_SHELL = re.compile(r"(`|\$\(|\$\{|\r|\n)")


def check_bash(cmd, scripts):
    if not scripts:
        raise Deny("this agent has no approved shell scripts")
    if BAD_SHELL.search(cmd):
        raise Deny("shell substitution or multi-line command not allowed")
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    try:
        toks = list(lex)
    except ValueError as exc:
        raise Deny("unparseable command: %s" % exc)
    if any(t and all(c in "();<>|&" for c in t) for t in toks):
        raise Deny("pipes, redirects, chaining or subshells not allowed")
    i = 0
    if toks and re.fullmatch(r"(pwsh|powershell)(\.exe)?", toks[0], re.I):
        i = 1
    while i < len(toks) and toks[i].lower() in ("-noprofile", "-noninteractive"):
        i += 1
    if i < len(toks) and toks[i].lower() == "-file":
        i += 1
    if i >= len(toks):
        raise Deny("no script given")
    script = toks[i].replace("\\", "/")
    script = re.sub(r"^\./", "", script)
    allowed = [("scripts/" + s).lower() for s in scripts]
    abs_allowed = [(ROOT.replace("\\", "/") + "/scripts/" + s).lower() for s in scripts]
    if script.lower() not in allowed and script.lower() not in abs_allowed:
        raise Deny("script not on this agent's allowlist: " + script)
    args = toks[i + 1:]
    # Elevated tool grants and unattended switches are for the owner only.
    for a in args:
        if re.fullmatch(r"-(AllowElevatedTools|Force|Confirm:\$false)", a, re.I):
            raise Deny("owner-only switch: " + a)
    # new-agent.ps1: a tools list may only contain the agent_allowed_tools minus Bash/WebFetch
    for k, a in enumerate(args):
        if a.lower() == "-tools" and k + 1 < len(args):
            tools = [t.strip() for t in args[k + 1].split(",") if t.strip()]
            ok = {"Read", "Write", "Edit", "Glob", "Grep"}
            bad = [t for t in tools if t not in ok]
            if bad:
                raise Deny("new agents may not be granted: " + ",".join(bad) + " (owner only)")
    # no secrets or paths as arguments
    for a in args:
        if is_secret(a):
            raise Deny("secret-like argument")


def check_web(url, hosts):
    host = (urlparse(url).hostname or "").lower()
    if urlparse(url).scheme != "https" or not any(fnmatch(host, h) for h in hosts):
        raise Deny("host not allowed: " + (host or url))


def decide(payload, mode):
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input", {}) or {}
    cwd = payload.get("cwd") or ROOT
    name = mode

    # ---- main session (owner): secrets only
    if name is None:
        probe = " ".join(str(ti.get(k, "")) for k in ("file_path", "path", "command", "pattern", "notebook_path"))
        if tool in ("Read", "Grep", "Glob", "Edit", "Write", "NotebookEdit") and is_secret(probe):
            raise Deny("secret-like path (owner session): " + probe[:100])
        if tool == "Bash" and re.search(r"\.secrets|\.env\b|sendgrid_api_key", probe):
            raise Deny("command touches secrets: " + probe[:100])
        if tool in ("Bash", "PowerShell") and re.search(r"\b(sqlcmd|invoke-sqlcmd|ssms)\b", probe, re.I):
            raise Deny("database tools are not used from the Team workspace; use the project session with its own guard")
        return "main-ok"

    # ---- agent session
    if not NAME_RE.fullmatch(name):
        raise Deny("bad agent name")
    prof, roots = profile_for(name)
    if tool not in POLICY["agent_allowed_tools"]:
        raise Deny("tool not permitted for agents: " + tool)

    if tool in ("Write", "Edit"):
        check_write(ti.get("file_path", ""), name, cwd, roots)
    elif tool in ("Read", "Glob", "Grep"):
        for key in ("file_path", "path"):
            if ti.get(key) and is_secret(norm(ti[key], cwd)):
                raise Deny("secret-like path")
        if ti.get("glob") and is_secret(str(ti["glob"])):
            raise Deny("secret-like glob")
        if tool in ("Glob", "Grep") and is_secret(str(ti.get("pattern", ""))) and tool == "Glob":
            raise Deny("secret-like pattern")
    elif tool == "Bash":
        check_bash(ti.get("command", ""), prof.get("bash_scripts", []))
    elif tool == "WebFetch":
        check_web(ti.get("url", ""), prof.get("web_hosts", []))
    return "agent-ok"


def main():
    argv = sys.argv[1:]
    mode = None
    if "--agent" in argv:
        mode = argv[argv.index("--agent") + 1]
    raw = sys.stdin.read()
    agent_label = mode or "?"
    try:
        payload = json.loads(raw) if raw.strip() else {}
        if mode == "auto":
            mode = payload.get("agent_type") or None
        agent_label = mode or "main"
        tool = payload.get("tool_name", "")
        try:
            reason = decide(payload, mode)
        except Deny as exc:
            log(agent_label, tool, "DENY", str(exc), json.dumps(payload.get("tool_input", {}))[:160])
            sys.stderr.write("TEAM GUARD blocked %s for %s: %s\n" % (tool, agent_label, exc))
            return 2
        log(agent_label, tool, "ok", reason, json.dumps(payload.get("tool_input", {}))[:100])
        return 0
    except Exception as exc:  # noqa: BLE001
        log(agent_label, "?", "ERROR", repr(exc))
        if mode not in (None, "auto"):
            sys.stderr.write("TEAM GUARD error, failing closed for %s: %r\n" % (agent_label, exc))
            return 2
        return 0


if __name__ == "__main__":
    sys.exit(main())
