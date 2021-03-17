#!/bin/bash

number=$(( RANDOM % 100))
guessNumber=101
guessAmount=0

while [ "$guessNumber" != "$number" ]; do
  read -p "guess the number?" guessNumber
  if [ "$guessNumber" -gt "$number" ]; then
    echo "that is too high"
  else
    echo "that is too low"
  fi
  ((guessAmount++))
done
echo "correct! the number was $number. you guessed it in $guessAmount tries"
