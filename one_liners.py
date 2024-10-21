print(''.join(f"{'\x0304' if i % 2 == 0 else '\x0307'}{c}" for i, c in enumerate("hadokn")))
print(''.join(f'\x030{5*(i%3)**2-8*(i%3)+3}{c}' for i,c in enumerate('hadokn')))
import random; print(f"\x03{random.randint(0, 15)}" + random.choice([r'¯\_(ツ)_/¯', 'ヽ(´ー｀)┌', r'¯\(°_o)/¯', '乁( •_• )ㄏ', '┐(´д｀)┌', 'it really tied the room together']) + "\x03")
