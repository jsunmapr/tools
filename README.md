Introduction:

This is an utility to be executed on data node to turn on UCS disk LED if MapR
detects the disk is sick, possibly before UCS detects it at HW level

Prerequisite:
 - LSI MegaCLI utilities (Or StorCLI)
 - All nodes must be able to do passwordless ssh to itself

Instruction:
 - Run this script on all nodes periodically using tool like crontab

