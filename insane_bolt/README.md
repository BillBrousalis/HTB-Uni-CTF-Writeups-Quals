# Insane Bolt (Misc) Writeup
This was a **programming** challenge.

![alt text](https://github.com/BillBrousalis/htb_uni_ctf_writeups/blob/main/insane_bolt/screenshots/insanebolt_maze.png)

We were given a maze of emojis, and asked to provide directions (ex. "DLLDRD")
so that the robot can reach the gem, while taking the shortest possible path.

The answer needed to be given within a few seconds, and we needed to pass
500 randomly generated levels in order to get the flag.

If we look at multiple generated mazes carefully, we can spot something;
There is never a need for the robot to move UP, not even in the navigation process.
This simplifies the problem a lot, since there is no need to use something like a 
breadth-first-search algorightm anymore.

### The logic used
We will have our robot navigate the maze in a certain way, until it finds
its way to the gem, while also keeping a record of the steps taken (ex. "DLRDDLLRD").
When the destination is reached, removing any wasted moves from our steps will result
in the shortest path possible.
For example, if we reach the gem after taking the steps DDLLLRRRRDDLD,
we only need to remove the wasted side movements and we get the solution:
DDLLLRRRRDDLD ==> DDRDDLD (removed LLLRRR, since they cancel each other out)

And there we have it. The code is available for more details.

![alt text](https://github.com/BillBrousalis/htb_uni_ctf_writeups/blob/main/insane_bolt/screenshots/insanebolt_flag.png)
