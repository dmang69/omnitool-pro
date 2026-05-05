toolkit:
  name: "Legitimate Device Repair Toolkit"
  version: "1.0.0"
filesystem:
  sandbox_root: "."
  max_depth: 10
automation:
  sandbox_enabled: true
  allowed_commands:
    - "adb"
    - "fastboot"
    - "powercfg"
    - "wmic"
security:
  path_sandboxing: true
  restricted_paths:
    - "C:\\Windows"
    - "/etc"
  audit_log: "logs/audit.log"
logging:
  level: "INFO"
  file: "logs/toolkit.log"