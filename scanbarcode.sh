#!/bin/bash

# go to correct directory
clear
sym=`readlink ${BASH_SOURCE[0]}`
if [[ "$sym" == "" ]]
  then
    # printf "Original"
    parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
    cd "$parent_path"
  else
    # printf "Not Original"
    parent_path=$( cd "$(dirname "${sym}")" ; pwd -P )
    cd "$parent_path"
  fi

barcode=""
timer=0
printf "0" > ".timer.txt"

# printf "Path: ${parent_path}"

function getbarcode {
  # printf -n "Enter character: "
  # printf -n ""
  stty cbreak
  char=`dd if=/dev/tty bs=100 count=1 2>/dev/null`
  stty -cbreak
  barcode="$barcode$char"
  # printf " Character was: $char"
  if [[ "${barcode: -1}" == "	" ]]
  then
      barcode="${barcode::${#barcode}-1}"
      clear
      printf "\nBarcode: $barcode\n"
      findindex $barcode
      barcode=""
      # printf $timer
      reset
  fi
}

function findindex {
  ./scanbarcode.py "scan" "$1"
}

function reset {
  timer=`cat .timer.txt`
  if [[ "$timer" == 0 ]]
  then
    printf "10" > ".timer.txt"
    # printf "Running..."
    runtimer &
    return
  fi
  printf "10" > ".timer.txt"
  # printf "test"
}

function runtimer {
  timer=`cat .timer.txt`
  # printf $tim123456 er
  if [[ "$timer" > 0 ]]
  then
    timer=$((timer-1))
    printf "$timer" > ".timer.txt"
    sleep 1 && runtimer
  elif [[ "$timer" < 1 ]]
  then
    clear
    printf "\nPlease Scan Id...\n"
    printf "" > ".current.txt"
    timer=0
  fi
}


function admin {
  printf "Admin Mode:\nPlease type (a) to add a person, (r) to remove a person, (ap) to add equipment, and (ab) to add barcode.\n> "
  read mode
  if [ "$mode" == "a" ] || [ "$mode" == "ap" ]
  then
    printf "\nEnter Name of new addition\n> "
    read name
    printf "\nScan barcode then press enter\n> "
    read barcode
    # barcode="${barcode::${#barcode}-1}"
      if [ "$mode" == "a" ]
    then
      ./scanbarcode.py "addp" "$name" "$barcode"
    else
      ./scanbarcode.py "adde" "$name" "$barcode"
    fi

  elif [ "$mode" == "ab" ]
  then
    ./scanbarcode.py "index"
    printf "\nPlease type in Id of which the new barcode should be added to\n> "
    read id
    printf "\nScan barcode then press enter\n> "
    read barcode
    # barcode="${barcode::${#barcode}-1}"
    ./scanbarcode.py "addb" $id "$barcode"
  fi
}


for arg in "$@"
do
  if [ "$arg" == "--admin" ] || [ "$arg" == "-a" ]
  then
    while true
    do
      admin
    done
    printf "\n\nAn Error has occured. Please reset. "
  fi
done


printf "\nPlease Scan Id...\n"

while true
do
  getbarcode
done
