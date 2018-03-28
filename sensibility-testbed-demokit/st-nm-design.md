# Sensibility Testbed nodemanager design proposal

## Introduction

This document proposes to extend the existing Seattle Testbed nodemanager 
component to allow for multi-party, fine-grained control over calls into 
the sensor-extended RepyV2 API that Sensibility Testbed sandboxes expose.

The idea is to let the Clearinghouse (as the nominal owner of the sandbox) 
and the donor (as the person that wants to protect their privacy) put in 
place and configure the frequency and accuracy at which a piece of 
experimenter code can read out sensor values. The technical implementation 
for restricting this is called 
[security layers](https://github.com/SeattleTestbed/docs/blob/master/Programming/SecurityLayers.wiki).


## Who, where, when?

There are multiple points in time when call restrictions can be put in 
place and modified by different parties. The lowest rate and accuracy 
for a call "wins".
The possible points in time to configure restrictions are, from early 
to late,
* (Donor at install time of the app --- this would be the absolute maximum 
  rate/accuracy that the donor feels comfortable with)
* Owner at vessel creation time --- this maps the experimenter's IRB
* Donor at experiment runtime --- donor may set different restrictions 
  for different experiments
* (Owner at experiment runtime --- Possible, but why?)

If restrictions are to be changed while an experiment runs, the experiment 
is stopped and the restrictions are updated. It is up to the experimenter 
(or their monitoring/deployment system) to restart the experiment on the 
device.


## The privilege gradient

Experimenter code cannot override or bypass the restrictions set by the 
Clearinghouse, nor can the Clearinghouse restrictions override the donor's. 
This means that whatever code and configuration the Clearinghouse has for 
this vessel, it must live in a space not accessible by experimenter code. 
(We can argue whether *read* access to the CH's vessel config is acceptable; 
*write* access clearly isn't, so as to keep the experiment from overriding 
them). Similarly, it must be impossible for the Clearinghouse restrictions to 
override the donor's.


## Implementation status

At the time of writing, the Seattle/Sensibility nodemanager does support 
two differently-privileged types of access to vessels, viz. *owner* and 
*user*. A vessel owner may modify (1) the owner public key itself, (2) the 
list of user public keys for this vessel, (3) the `ownerinfo` string for 
this vessel. Other than that, the owner's privileges are identical with 
a vessel user's. A vessel user may upload/download/list files, start/stop 
experiment code, inspect the vessel log, and reset the vessel. A prototype 
filename-based privilege separation layer exists (for names that start with 
`private_`), the implementation is incomplete and badly designed.

The donor should be able to configure the `repy-prepend` and `repy-prepend-dir` 
flags that the sandbox takes, but they are not exposed through the installer 
(shell or GUI), and the sandbox probably wouldn't respect them anyway.
