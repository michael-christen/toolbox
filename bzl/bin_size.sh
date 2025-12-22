#!/bin/bash
# Modification of:
# https://interrupt.memfault.com/blog/best-firmware-size-tools
#
# XXX: Cleanup
set -e

if [  $# -le 2 ]
then
    echo "This script requires 5 arguments."
    echo -e "\nUsage:\nget-fw-size TOOL FILE BAZEL_LABEL MAX_FLASH_SIZE MAX_RAM_SIZE \n"
    exit 1
fi

tool=$1
file=$2
bazel_label=$3
max_flash=$4
max_ram=$5

raw=$($tool $file)

text=$(echo $raw | cut -d ' ' -f 7)
data=$(echo $raw | cut -d ' ' -f 8)
bss=$(echo $raw | cut -d ' ' -f 9)

flash=$(($text + $data))
ram=$(($data + $bss))

# XXX: Maybe normalize the label
# XXX: Likely not escaped properly ..., use jq?
cat <<EOF
{
  "label": "${bazel_label}",
  "text": ${text},
  "data": ${data},
  "bss": ${bss},
  "max_flash": ${max_flash},
  "flash": ${flash},
  "max_ram": ${max_ram},
  "ram": ${ram}
}
EOF
