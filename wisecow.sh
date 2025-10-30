#!/usr/bin/env bash

SRVPORT=4499
RSPFILE=response

# Ensure pipe is removed on exit
cleanup() {
    rm -f "$RSPFILE"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

get_api() {
    read line
    echo "$line"
}

handleRequest() {
    # 1) Process the request
    get_api
    mod=$(fortune)

    cat <<EOF > "$RSPFILE"
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close

<pre>$(cowsay "$mod")</pre>
EOF
}

prerequisites() {
    command -v cowsay >/dev/null 2>&1 &&
    command -v fortune >/dev/null 2>&1 || 
        { 
            echo "Install prerequisites." >&2
            exit 1
        }
}

main() {
    prerequisites
    echo "Wisdom served on port=${SRVPORT}..."

    rm -f "$RSPFILE"
    mkfifo "$RSPFILE"

    while true; do
        # Use -l -p compatibility; -N for close on EOF (available on netcat-openbsd)
        cat "$RSPFILE" | nc -lN "$SRVPORT" | handleRequest
        sleep 0.01
    done
}

main
