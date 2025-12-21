#!/bin/bash
# Modification of:
# https://interrupt.memfault.com/blog/best-firmware-size-tools
#
# XXX: Cleanup
set -e

if [  $# -le 2 ]
then
    echo "This script requires 4 arguments."
    echo -e "\nUsage:\nget-fw-size TOOL FILE MAX_FLASH_SIZE MAX_RAM_SIZE \n"
    exit 1
fi

tool=$1
file=$2
max_flash=$3
max_ram=$4

function print_region() {
    size=$1
    max_size=$2
    name=$3

    if [[ $max_size == 0x* ]];
    then
        max_size=$(echo ${max_size:2})
        max_size=$(( 16#$max_size ))
    fi

    pct=$(( 100 * $size / $max_size ))
    echo "$name used: $size / $max_size ($pct%)"
}

raw=$($tool $file)

text=$(echo $raw | cut -d ' ' -f 7)
data=$(echo $raw | cut -d ' ' -f 8)
bss=$(echo $raw | cut -d ' ' -f 9)

flash=$(($text + $data))
ram=$(($data + $bss))

echo "Text: ${text}"
echo "Data: ${data}"
echo "BSS: ${bss}"
print_region $flash $max_flash "Flash"
print_region $ram $max_ram "RAM"
