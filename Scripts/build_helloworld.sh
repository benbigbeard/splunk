#!/bin/bash

# Step 1: Set repo ZIP URL
ZIP_URL="https://github.com/benbigbeard/splunklib/archive/refs/heads/main.zip"

# Step 2: Build base structure
mkdir -p helloworld/bin helloworld/default helloworld/metadata

# Step 3: Create Python command
cat > helloworld/bin/helloworld.py << 'EOF'
#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "splunklib"))

from splunklib.searchcommands import StreamingCommand, Configuration, Option, dispatch

@Configuration()
class HelloWorldCommand(StreamingCommand):
    field = Option(require=True)

    def stream(self, records):
        for record in records:
            value = record.get(self.field, "")
            record["helloworld"] = f"hello {value}"
            yield record

dispatch(HelloWorldCommand, sys.argv, sys.stdin, sys.stdout, __name__)
EOF

# Step 4: Create conf files
cat > helloworld/default/commands.conf << 'EOF'
[helloworld]
filename = helloworld.py
chunked = true
supports_getinfo = true
outputheader = true
EOF

cat > helloworld/default/searchbnf.conf << 'EOF'
[helloworld-command]
syntax = HELLOWORLD FIELD=<field>
shortdesc = Returns a new field that says "hello <field value>".
description = \
    The helloworld command adds a new field called 'helloworld' that prepends 'hello ' to the value \
    of the specified field.
example1 = \
    | makeresults | eval name="Alice" | helloworld field=name
arguments.field = Required. The name of the field whose value will be prepended with "hello ".
category = streaming
usage = public
appears-in = 1.0
maintainer = you
EOF

cat > helloworld/default/props.conf << 'EOF'
[search-commands]
EXTRACT-command = (?i)^\s*(helloworld)\b
EOF

cat > helloworld/metadata/default.meta << 'EOF'
[]
access = read : [ * ], write : [ admin, power ]
export = system

[searchbnf]
export = system
EOF

# Step 5: Download and extract only splunklib/ from repo ZIP
echo "Downloading splunklib from GitHub..."
curl -L -o /tmp/splunklib_repo.zip "$ZIP_URL"
unzip -qo /tmp/splunklib_repo.zip "splunklib-main/splunklib/*" -d /tmp/
mv /tmp/splunklib-main/splunklib helloworld/bin/
rm -rf /tmp/splunklib_repo.zip /tmp/splunklib-main

echo "helloworld app created with splunklib"