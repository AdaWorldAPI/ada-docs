#!/bin/bash
# ada-blackboard.sh — Real-time cross-session collaboration via Upstash Redis
# Source this in Claude Code: source /tmp/ada-docs/scripts/ada-blackboard.sh

# Config (override via env)
UPSTASH_URL="${UPSTASH_URL:-https://upright-jaybird-27907.upstash.io}"
UPSTASH_TOKEN="${UPSTASH_TOKEN:-AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc}"
BB_REPO="${BB_REPO:-$(basename $PWD)}"
BB_SESSION="${BB_SESSION:-$(cat /tmp/.bb_session_id 2>/dev/null || uuidgen | tee /tmp/.bb_session_id)}"

# Redis command helper
bb_cmd() {
  curl -s -X POST "$UPSTASH_URL" \
    -H "Authorization: Bearer $UPSTASH_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"command\": $1}"
}

# ─────────────────────────────────────────────────────────────────
# SESSION MANAGEMENT
# ─────────────────────────────────────────────────────────────────

bb_register() {
  # Register this session in bb:sessions
  local ts=$(date +%s)
  bb_cmd "[\"HSET\", \"bb:sessions\", \"$BB_SESSION\", \"{\\\"repo\\\":\\\"$BB_REPO\\\",\\\"started\\\":$ts,\\\"last_seen\\\":$ts}\"]"
  echo "Session registered: $BB_SESSION ($BB_REPO)"
}

bb_heartbeat() {
  # Update last_seen timestamp
  local ts=$(date +%s)
  local current=$(bb_cmd "[\"HGET\", \"bb:sessions\", \"$BB_SESSION\"]" | jq -r '.result // empty')
  if [ -n "$current" ]; then
    local updated=$(echo "$current" | jq -c ".last_seen = $ts")
    bb_cmd "[\"HSET\", \"bb:sessions\", \"$BB_SESSION\", $(echo "$updated" | jq -Rs .)]"
  fi
}

bb_deregister() {
  # Remove session on exit
  bb_cmd "[\"HDEL\", \"bb:sessions\", \"$BB_SESSION\"]"
  echo "Session deregistered: $BB_SESSION"
}

bb_list_sessions() {
  # Show all active sessions
  bb_cmd "[\"HGETALL\", \"bb:sessions\"]" | jq -r '.result | to_entries | .[] | "\(.key): \(.value)"'
}

# ─────────────────────────────────────────────────────────────────
# BLACKBOARD APPEND
# ─────────────────────────────────────────────────────────────────

bb_post() {
  # Generic post to a stream
  # Usage: bb_post <stream> <field1> <value1> <field2> <value2> ...
  local stream="$1"
  shift
  local fields="\"sid\", \"$BB_SESSION\", \"repo\", \"$BB_REPO\", \"ts\", \"$(date +%s%3N)\""
  while [ $# -gt 0 ]; do
    fields="$fields, \"$1\", \"$2\""
    shift 2
  done
  bb_cmd "[\"XADD\", \"$stream\", \"*\", $fields]"
}

bb_edit() {
  # Post an edit to repo blackboard
  # Usage: bb_edit <path> <op> <line> <content> [context]
  local path="$1"
  local op="$2"
  local line="$3"
  local content="$4"
  local context="${5:-}"
  
  bb_post "bb:$BB_REPO" \
    "type" "edit" \
    "path" "$path" \
    "op" "$op" \
    "line" "$line" \
    "content" "$(echo "$content" | base64 -w0)" \
    "context" "$context"
  
  echo "Posted edit: $path:$line ($op)"
}

bb_insight() {
  # Post a design insight to global
  # Usage: bb_insight <category> <title> <body> [affects]
  local category="$1"
  local title="$2"
  local body="$3"
  local affects="${4:-$BB_REPO}"
  
  bb_post "bb:global" \
    "type" "insight" \
    "category" "$category" \
    "title" "$title" \
    "body" "$(echo "$body" | base64 -w0)" \
    "affects" "$affects"
  
  echo "Posted insight: [$category] $title"
}

bb_contract() {
  # Post a contract update
  # Usage: bb_contract <contract> <change> <target> <details_json>
  local contract="$1"
  local change="$2"
  local target="$3"
  local details="$4"
  
  bb_post "bb:contracts" \
    "type" "contract" \
    "contract" "$contract" \
    "change" "$change" \
    "target" "$target" \
    "details" "$(echo "$details" | base64 -w0)"
  
  echo "Posted contract update: $contract.$target ($change)"
}

bb_request() {
  # Request action from another repo
  # Usage: bb_request <to_repo> <action> <what> [priority]
  local to_repo="$1"
  local action="$2"
  local what="$3"
  local priority="${4:-medium}"
  
  bb_post "bb:global" \
    "type" "request" \
    "to_repo" "$to_repo" \
    "action" "$action" \
    "what" "$what" \
    "priority" "$priority" \
    "callback" "bb:$BB_REPO"
  
  echo "Requested: $to_repo → $action: $what"
}

bb_ack() {
  # Acknowledge a request
  # Usage: bb_ack <request_id> <status> [notes]
  local request_id="$1"
  local status="$2"
  local notes="${3:-}"
  
  bb_post "bb:global" \
    "type" "ack" \
    "request_id" "$request_id" \
    "status" "$status" \
    "notes" "$notes"
  
  echo "Acknowledged: $request_id → $status"
}

# ─────────────────────────────────────────────────────────────────
# BLACKBOARD READ
# ─────────────────────────────────────────────────────────────────

bb_read() {
  # Read recent entries from a stream
  # Usage: bb_read <stream> [count]
  local stream="$1"
  local count="${2:-20}"
  
  bb_cmd "[\"XREVRANGE\", \"$stream\", \"+\", \"-\", \"COUNT\", \"$count\"]" | \
    jq -r '.result[] | "\(.[0]): \(.[1] | map(.) | join(" "))"'
}

bb_read_repo() {
  # Read this repo's blackboard
  bb_read "bb:$BB_REPO" "${1:-20}"
}

bb_read_global() {
  # Read global broadcasts
  bb_read "bb:global" "${1:-20}"
}

bb_read_contracts() {
  # Read contract updates
  bb_read "bb:contracts" "${1:-20}"
}

bb_read_insights() {
  # Read recent insights (filter global for type=insight)
  bb_cmd "[\"XREVRANGE\", \"bb:global\", \"+\", \"-\", \"COUNT\", \"50\"]" | \
    jq -r '.result[] | select(.[1] | index("type") as $i | .[($i+1)] == "insight") | "\(.[0]): \(.[1] | map(.) | join(" "))"'
}

bb_read_requests() {
  # Read pending requests for this repo
  bb_cmd "[\"XREVRANGE\", \"bb:global\", \"+\", \"-\", \"COUNT\", \"50\"]" | \
    jq -r --arg repo "$BB_REPO" '.result[] | select(.[1] | index("to_repo") as $i | .[($i+1)] == $repo) | "\(.[0]): \(.[1] | map(.) | join(" "))"'
}

# ─────────────────────────────────────────────────────────────────
# LOCKING
# ─────────────────────────────────────────────────────────────────

bb_lock() {
  # Acquire lock on a file (60s TTL)
  # Usage: bb_lock <path>
  local path="$1"
  local key="bb:lock:$BB_REPO:$path"
  
  local result=$(bb_cmd "[\"SET\", \"$key\", \"$BB_SESSION\", \"NX\", \"EX\", \"60\"]" | jq -r '.result')
  
  if [ "$result" = "OK" ]; then
    echo "Lock acquired: $path"
    return 0
  else
    local holder=$(bb_cmd "[\"GET\", \"$key\"]" | jq -r '.result')
    echo "Lock held by: $holder"
    return 1
  fi
}

bb_unlock() {
  # Release lock
  # Usage: bb_unlock <path>
  local path="$1"
  local key="bb:lock:$BB_REPO:$path"
  
  bb_cmd "[\"DEL\", \"$key\"]"
  echo "Lock released: $path"
}

bb_extend_lock() {
  # Extend lock TTL (call every 30s while editing)
  # Usage: bb_extend_lock <path>
  local path="$1"
  local key="bb:lock:$BB_REPO:$path"
  
  bb_cmd "[\"EXPIRE\", \"$key\", \"60\"]"
}

# ─────────────────────────────────────────────────────────────────
# QUICK STATUS
# ─────────────────────────────────────────────────────────────────

bb_status() {
  echo "=== Blackboard Status ==="
  echo "Session: $BB_SESSION"
  echo "Repo: $BB_REPO"
  echo ""
  echo "Active Sessions:"
  bb_list_sessions
  echo ""
  echo "Recent Global (last 5):"
  bb_read_global 5
  echo ""
  echo "Pending Requests for $BB_REPO:"
  bb_read_requests
}

# ─────────────────────────────────────────────────────────────────
# INIT
# ─────────────────────────────────────────────────────────────────

echo "Ada Blackboard loaded."
echo "  Session: $BB_SESSION"
echo "  Repo: $BB_REPO"
echo ""
echo "Commands: bb_register, bb_edit, bb_insight, bb_contract, bb_request, bb_ack"
echo "          bb_read_repo, bb_read_global, bb_read_contracts, bb_status"
echo "          bb_lock, bb_unlock, bb_list_sessions"
