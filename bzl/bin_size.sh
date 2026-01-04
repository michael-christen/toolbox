#!/bin/bash
# Modification of:
# https://interrupt.memfault.com/blog/best-firmware-size-tools
#
# XXX: Cleanup
set -e

if [  $# -le 2 ]
then
    echo "This script requires 5 arguments."
    echo -e "\nUsage:\nbin_size.sh TOOL FILE BAZEL_LABEL MAX_FLASH_SIZE MAX_RAM_SIZE \n"
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

# Note that we haven't normalized the label, and there's a chance our data here
# may not yet be escaped properly, if this occurs we could end up with
# improperly formatted json or even misinterpreted results. We're ok with that
# for now, but sanitizing this information would be a welcome cleanup.
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
