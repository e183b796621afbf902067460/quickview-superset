#!/bin/bash

for script in docker-entrypoint-initdb.d/*
  do
    if [[ $script == *.sh ]]; then
      bash "$script"
    fi
  done
