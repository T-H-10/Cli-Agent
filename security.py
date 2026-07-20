import re

def static_check(command):
    # Normalize command for easier checking
    clean_cmd = " ".join(command.lower().split())
    
    danger_patterns = {
        # --- Linux / bash ---
        r"rm\s+-[rf]{1,2}\s+/": "Attempt to delete the root directory.",
        r"rm\s+-[rf]{1,2}\s+": "Recursive/forced file deletion (rm -rf).",
        r"mkfs": "Attempt to format a disk.",
        r":\(\)\{\s*:\|:&\s*\};:": "Fork bomb (denial of service).",
        r"chmod\s+777": "Opening full permissions (security risk).",
        r"> /dev/sd": "Directly overwriting hardware partitions.",
        # --- Windows CMD ---
        r"\bformat\s+[a-z]:": "Attempt to format a drive.",
        r"\bshutdown\b": "Attempt to shut down or restart the machine.",
        r"\bdel\s+/[fqs]": "Forced/quiet file deletion (del /f, /q).",
        r"\bdel\s+.*\*": "Bulk file deletion with wildcard (del *).",
        r"\b(rd|rmdir)\s+/s": "Recursive directory deletion (rd /s).",
        r"\bdiskpart\b": "Disk partitioning utility (diskpart).",
    }

    for pattern, reason in danger_patterns.items():
        if re.search(pattern, clean_cmd):
            return False, f"⚠️ BLOCKING: {reason}"
    
    return True, None


def llm_security_audit(command, client):
    security_prompt = """
    You are a security auditor. Analyze the following CLI command for destructive intent.
    If the command is safe, return 'SAFE'.
    If it is dangerous (e.g., deletes data, exposes secrets, crashes system), return 'DANGEROUS: [Reason]'.
    Command: """
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": security_prompt + command}],
            max_tokens=50
        )
        result = response.choices[0].message.content.strip()
        return result
    except:
        return "SAFE" # Fallback if API fails
    
    
def validate_command(command, client):
    # 1. Quick Static Check
    is_ok, reason = static_check(command)
    if not is_ok:
        return False, reason

    # 2. Contextual LLM Audit
    audit_result = llm_security_audit(command, client)
    if audit_result.startswith("DANGEROUS"):
        return False, f"⚠️ {audit_result}"

    return True, command