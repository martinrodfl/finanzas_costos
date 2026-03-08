CR = bytes([0x0d])   # carriage return
VT = bytes([0x0b])   # vertical tab

with open('install.bat', 'rb') as f:
    raw = f.read()

fixed = raw

# Corregir api\venv con vertical tab (0x0b) en lugar de backslash+v
fixed = fixed.replace(b'api' + VT + b'env', b'api\\venv')
fixed = fixed.replace(b'apivenv', b'api\\venv')

# Corregir api\requirements con CR (0x0d) en lugar de backslash+r
fixed = fixed.replace(b'api' + CR + b'equirements.txt', b'api\\requirements.txt')

with open('install.bat', 'wb') as f:
    f.write(fixed)

print('Correcciones aplicadas.')

# Verificar byte a byte las lineas 78-86
lines = fixed.split(b'\r\n')
print()
for i in range(77, min(87, len(lines))):
    out = ''
    for b in lines[i]:
        if 32 <= b <= 126:
            out += chr(b)
        else:
            out += f'[{b:02x}]'
    print(f'L{i+1}: {out}')
