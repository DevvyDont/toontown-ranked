@echo off
title Toontown Ranked - Launcher

echo Starting Servers
start start_servers.bat

TIMEOUT /T 2
echo Starting Client
start start_client.bat