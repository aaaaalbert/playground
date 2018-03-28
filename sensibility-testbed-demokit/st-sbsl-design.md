# Sensibility Testbed sandbox security layer design proposal

## Introduction

This document discusses ideas to allow different parties (with different 
associated privileges) to add security layers to a sandbox. The privilege 
gradient requires that security layers from different parties must be 
isolated from one another.

Also, the nodemanager must know about and be able to handle the setup. 
This includes remembering state, e.g. which security layer to use for 
what party, and where to read it from. The nodemanager aspects are discussed 
in a separate doc though, https://github.com/aaaaalbert/repy-doodles/blob/master/st-nm-design.md

## High-level view
Let's assume we have two parties that may splice in security layers before the 
user program runs: the donor and the vessel owner. The Repy file API doesn't 
allow us to read files from different directories, but the sandbox launch code 
could be modified to switch directories after instantiating each party's layers.
(The various layers could be uploaded to different vessels that aren't accessible 
from one another if the owner/user keys are set up appropriately.)

We could signal the security layer config to the sandbox like so:

```
python repy.py restrictionsfile --donor-seclayer-dir ../v17 --donor-seclayers
encasementlib.r2py onelayer.r2py anotherlayer.r2py --owner-seclayer-dir ../v876 
--owner-seclayers encasementlib.r2py additionallayer.r2py --user-prog-cwd ../v3
--user-prog myprogram.r2py user program args follow here
```

(Relevant code to loop over: https://github.com/SeattleTestbed/repy_v2/blob/master/repy.py#L306-L380 )

In the loop,
* change dir to the next seclayer dir
* run seclayer program with args
* store the `context` that this virtual namespace returns. From there, the 
overridden calls can be passed on to the next layer/program.


## Problems
* It's not great to force the clearinghouse to keep state (in terms of which 
vessel contains what seclayer). However, it's probably worse if we force the 
burden onto the nodemanager.
* Changing dirs while programs run is problematic if the code decides to access
files after we leave its dir. This significantly impacts what security layers can 
do, and opens them to possible data/code corruption.
* Whose restrictions should be used when a security layer is spliced in? Would the 
seclayers' vessel dirs have/need/use their own resource restrictions files?
