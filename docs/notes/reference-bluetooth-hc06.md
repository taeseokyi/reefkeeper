# reference-bluetooth-hc06

> "HC-06 블루투스 WSL 연결 방법 — rfcomm, MAC 주소"

---

**HC-06 MAC:** `98:DA:60:0F:C5:7A`

**WSL에서 연결 순서:**
1. Windows PowerShell (관리자): `usbipd bind --busid 1-1` (최초 1회)
2. Windows PowerShell: `usbipd attach --wsl --busid 1-1` (재시작 시마다)
3. WSL: `sudo service bluetooth start`
4. WSL: `sudo rfcomm release rfcomm0` (기존 bind 있을 때)
5. WSL: `sudo rfcomm connect rfcomm0 98:DA:60:0F:C5:7A 1`
   → "Connected /dev/rfcomm0 ..." 메시지 후 터미널 유지 (또는 nohup 백그라운드)

**주의사항:**
- HC-06은 1:1 연결 — 폰 앱 연결 중이면 PC에서 접속 불가, 폰 먼저 끊을 것
- rfcomm connect 터미널 닫으면 연결 끊김
- bluetoothctl trust 설정 필요: `bluetoothctl trust 98:DA:60:0F:C5:7A`

**연결 확인:**
```bash
python3 -c "import serial,time; s=serial.Serial('/dev/rfcomm0',9600,timeout=3); time.sleep(1); s.write(b'status\r\n'); time.sleep(2); [print(s.readline().decode().strip()) for _ in range(20) if s.in_waiting]"
```
