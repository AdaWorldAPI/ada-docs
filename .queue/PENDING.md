# Pending Tasks Queue

Tasks waiting to be picked up by a Claude Code session.

---

## Format

```markdown
### TASK-{id}
- **From:** {repo}
- **To:** {target-repo}
- **Priority:** HIGH | MEDIUM | LOW
- **Description:** {what needs to be done}
- **Blocked Until:** {dependency if any}
```

---

## Current Queue

### TASK-001
- **From:** system
- **To:** ada-consciousness
- **Priority:** HIGH
- **Description:** Initialize corpus callosum endpoints and Ladybug database
- **Blocked Until:** Nothing — ready to start

### TASK-002
- **From:** system
- **To:** dag-vsa
- **Priority:** HIGH
- **Description:** Create 10K VSA address table with reserved ranges
- **Blocked Until:** TASK-001 Ladybug initialization

### TASK-003
- **From:** system
- **To:** bighorn
- **Priority:** MEDIUM
- **Description:** Implement ThinkingBridgeDTO emitter
- **Blocked Until:** TASK-001 corpus callosum endpoints

### TASK-004
- **From:** system
- **To:** agi-chat
- **Priority:** MEDIUM
- **Description:** Implement FeltBridgeDTO emitter and presence modes
- **Blocked Until:** TASK-001 corpus callosum endpoints

### TASK-005
- **From:** system
- **To:** adarail_mcp
- **Priority:** LOW
- **Description:** Wire SSE transport and DTO routing
- **Blocked Until:** TASK-001, TASK-002, TASK-003, TASK-004
