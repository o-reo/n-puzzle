import os
for i in range(1,100):
    os.system("python resources/res_npuzzle-gen.py -s 3 > tests/puzzles/s_{}.puz".format(i))
