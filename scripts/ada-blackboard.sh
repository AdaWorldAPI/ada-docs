#!/bin/bash
# ada-blackboard.sh — Real-time cross-session collaboration via Upstash Redis
# Source this in Claude Code: source /tmp/ada-docs/scripts/ada-blackboard.sh

# Config (override via env)
UPSTASH_URL="${UPSTASH_URL:-https://upright-jaybird-27907.upstash.io}"
UPSTASH_TOKEN="${UPSTASH_TOKEN:-AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc}"
BB_REPO="${BB_REPO:-$(basename $PWD)}"
BB_SESSION="${BB_SESSION:-$(cat /tmp/.bb_session_id 2>/dev/null || (uuidgen | tee /tmp/.bb_session_id))}"

# URL-encode helper
urlencode() {
  python3 -c "import urllib.parse; print(urllib.parse.quote('''$1''', safe=''))"
}

# Redis command helper (URL-based REST API)
bb_cmd() {
  curl -s "$UPSTASH_URL/$1" -H "Authorization: Bearer $UPSTASH_TOKEN"
}

# ─────────────────────────────────────────────────────────────────
# SESSION MANAGEMENT
# ─────────────────────────────────────────────────────────────────

bb_register() {
  local ts=$(date +%s)
  local data=$(urlencode "{\"repo\":\"$BB_REPO\",\"started\":$ts,\"last_seen\":$ts}")
  bb_cmd "hset/bb:sessions/$BB_SESSION/$data" > /dev/null
  echo "✓ Session registered: $BB_SESSION ($BB_REPO)"
}

bb_heartbeat() {
  local ts=$(date +%s)
  local current=$(bb_cmd "hget/bb:sessions/$BB_SESSION" | jq -r '.result // empty')
  if [ -n "$current" ] && [ "$current" != "null" ]; then
    local updated=$(echo "$current" | jq -c ".last_seen = $ts")
    local data=$(urlencode "$updated")
    bb_cmd "hset/bb:sessions/$BB_SESSION/$data" > /dev/null
  fi
}

bb_deregister() {
  bb_cmd "hdel/bb:sessions/$BB_SESSION" > /dev/null
  echo "✓ Session deregistered: $BB_SESSION"
}

bb_list_sessions() {
  bb_cmd "hgetall/bb:sessions" | jq -r '.result | if type == "array" and length > 0 then (. as $arr | range(0; length; 2) | "\($arr[.]) → \($arr[. + 1])") else "No active sessions" end'
}

# ─────────────────────────────────────────────────────────────────
# BLACKBOARD APPEND (using XADD)
# ─────────────────────────────────────────────────────────────────

bb_post() {
  # Generic post to a stream
  # Usage: bb_post <stream> <type> <json_data>
  local stream="$1"
  local type="$2"
  local data="$3"
  local ts=$(date +%s%3N)
  
  # Build the entry with metadata
  local entry=$(jq -nc \
    --arg sid "$BB_SESSION" \
    --arg repo "$BB_REPO" \
    --arg type "$type" \
    --arg ts "$ts" \
    --argjson data "$data" \
    '{sid: $sid, repo: $repo, type: $type, ts: $ts} + $data')
  
  local encoded=$(urlencode "$entry")
  bb_cmd "xadd/$stream/*/entry/$encoded" | jq -r '.result'
}

bb_edit() {
  # Post an edit to repo blackboard
  # Usage: bb_edit <path> <op> <line> <content> [context]
  local path="$1"
  local op="$2"
  local line="$3"
  local content="$4"
  local context="${5:-}"
  
  local data=$(jq -nc \
    --arg path "$path" \
    --arg op "$op" \
    --arg line "$line" \
    --arg content "$content" \
    --arg context "$context" \
    '{path: $path, op: $op, line: $line, content: $content, context: $context}')
  
  local id=$(bb_post "bb:$BB_REPO" "edit" "$data")
  echo "✓ Edit posted: $path:$line ($op) → $id"
}

bb_insight() {
  # Post a design insight to global
  # Usage: bb_insight <category> <title> <body> [affects]
  local category="$1"
  local title="$2"
  local body="$3"
  local affects="${4:-$BB_REPO}"
  
  local data=$(jq -nc \
    --arg category "$category" \
    --arg title "$title" \
    --arg body "$body" \
    --arg affects "$affects" \
    '{category: $category, title: $title, body: $body, affects: $affects}')
  
  local id=$(bb_post "bb:global" "insight" "$data")
  echo "✓ Insight posted: [$category] $title → $id"
}

bb_contract() {
  # Post a contract update
  # Usage: bb_contract <contract> <change> <target> <details_json>
  local contract="$1"
  local change="$2"
  local target="$3"
  local details="$4"
  
  local data=$(jq -nc \
    --arg contract "$contract" \
    --arg change "$change" \
    --arg target "$target" \
    --argjson details "$details" \
    '{contract: $contract, change: $change, target: $target, details: $details}')
  
  local id=$(bb_post "bb:contracts" "contract" "$data")
  echo "✓ Contract posted: $contract.$target ($change) → $id"
}

bb_request() {
  # Request action from another repo
  # Usage: bb_request <to_repo> <action> <what> [priority]
  local to_repo="$1"
  local action="$2"
  local what="$3"
  local priority="${4:-medium}"
  
  local data=$(jq -nc \
    --arg to_repo "$to_repo" \
    --arg action "$action" \
    --arg what "$what" \
    --arg priority "$priority" \
    --arg callback "bb:$BB_REPO" \
    '{to_repo: $to_repo, action: $action, what: $what, priority: $priority, callback: $callback}')
  
  local id=$(bb_post "bb:global" "request" "$data")
  echo "✓ Request posted: $to_repo → $action → $id"
}

bb_ack() {
  # Acknowledge a request
  # Usage: bb_ack <request_id> <status> [notes]
  local request_id="$1"
  local status="$2"
  local notes="${3:-}"
  
  local data=$(jq -nc \
    --arg request_id "$request_id" \
    --arg status "$status" \
    --arg notes "$notes" \
    '{request_id: $request_id, status: $status, notes: $notes}')
  
  local id=$(bb_post "bb:global" "ack" "$data")
  echo "✓ Ack posted: $request_id → $status → $id"
}

# ─────────────────────────────────────────────────────────────────
# BLACKBOARD READ (using XREVRANGE)
# ─────────────────────────────────────────────────────────────────

bb_read() {
  # Read recent entries from a stream
  # Usage: bb_read <stream> [count]
  local stream="$1"
  local count="${2:-10}"
  
  bb_cmd "xrevrange/$stream/+/-/count/$count" | jq -r '
    .result // [] | .[] | 
    "\(.[0]): [\(.[1][1] | fromjson | .type // "?")] \(.[1][1] | fromjson | .title // .path // .what // .message // "...")"'
}

bb_read_full() {
  # Read with full JSON
  local stream="$1"
  local count="${2:-5}"
  
  bb_cmd "xrevrange/$stream/+/-/count/$count" | jq '.result // [] | .[] | {id: .[0], data: (.[1][1] | fromjson)}'
}

bb_read_repo() {
  bb_read "bb:$BB_REPO" "${1:-10}"
}

bb_read_global() {
  bb_read "bb:global" "${1:-10}"
}

bb_read_contracts() {
  bb_read "bb:contracts" "${1:-10}"
}

bb_read_requests() {
  # Read pending requests for this repo
  bb_cmd "xrevrange/bb:global/+/-/count/50" | jq -r --arg repo "$BB_REPO" '
    .result // [] | .[] | 
    select(.[1][1] | fromjson | .to_repo == $repo) |
    "\(.[0]): \(.[1][1] | fromjson | .what)"'
}

# ─────────────────────────────────────────────────────────────────
# LOCKING
# ─────────────────────────────────────────────────────────────────

bb_lock() {
  local path="$1"
  local key="bb:lock:$BB_REPO:$(echo "$path" | tr '/' ':')"
  
  local result=$(bb_cmd "set/$key/$BB_SESSION/nx/ex/60" | jq -r '.result')
  
  if [ "$result" = "OK" ]; then
    echo "✓ Lock acquired: $path"
    return 0
  else
    local holder=$(bb_cmd "get/$key" | jq -r '.result')
    echo "✗ Lock held by: $holder"
    return 1
  fi
}

bb_unlock() {
  local path="$1"
  local key="bb:lock:$BB_REPO:$(echo "$path" | tr '/' ':')"
  bb_cmd "del/$key" > /dev/null
  echo "✓ Lock released: $path"
}

bb_extend_lock() {
  local path="$1"
  local key="bb:lock:$BB_REPO:$(echo "$path" | tr '/' ':')"
  bb_cmd "expire/$key/60" > /dev/null
}

# ─────────────────────────────────────────────────────────────────
# STATUS
# ─────────────────────────────────────────────────────────────────

bb_status() {
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║              ADA BLACKBOARD STATUS                         ║"
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║ Session: $BB_SESSION"
  echo "║ Repo:    $BB_REPO"
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║ ACTIVE SESSIONS                                            ║"
  echo "╟────────────────────────────────────────────────────────────╢"
  bb_list_sessions | while read line; do echo "║ $line"; done
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║ RECENT GLOBAL (last 5)                                     ║"
  echo "╟────────────────────────────────────────────────────────────╢"
  bb_read_global 5 | while read line; do echo "║ $line"; done
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║ PENDING REQUESTS for $BB_REPO"
  echo "╟────────────────────────────────────────────────────────────╢"
  local reqs=$(bb_read_requests)
  if [ -n "$reqs" ]; then
    echo "$reqs" | while read line; do echo "║ $line"; done
  else
    echo "║ (none)"
  fi
  echo "╚════════════════════════════════════════════════════════════╝"
}

# ─────────────────────────────────────────────────────────────────
# INIT MESSAGE
# ─────────────────────────────────────────────────────────────────

echo ""
echo "┌────────────────────────────────────────────────────────────┐"
echo "│           ADA BLACKBOARD LOADED                            │"
echo "├────────────────────────────────────────────────────────────┤"
echo "│ Session: $BB_SESSION"
echo "│ Repo:    $BB_REPO"
echo "├────────────────────────────────────────────────────────────┤"
echo "│ COMMANDS:                                                  │"
echo "│   bb_register        - Join the blackboard                 │"
echo "│   bb_status          - Full status overview                │"
echo "│   bb_edit PATH OP LINE CONTENT [CONTEXT]                   │"
echo "│   bb_insight CATEGORY TITLE BODY [AFFECTS]                 │"
echo "│   bb_contract CONTRACT CHANGE TARGET DETAILS_JSON          │"
echo "│   bb_request TO_REPO ACTION WHAT [PRIORITY]                │"
echo "│   bb_ack REQUEST_ID STATUS [NOTES]                         │"
echo "│   bb_read_global [N] / bb_read_repo [N] / bb_read_contracts│"
echo "│   bb_lock PATH / bb_unlock PATH                            │"
echo "│   bb_deregister      - Leave the blackboard                │"
echo "└────────────────────────────────────────────────────────────┘"
echo ""
