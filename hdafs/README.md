afsbin
======

Scripts for Tier 1 AFS ([Andrew File System](http://en.wikipedia.org/wiki/Andrew_File_System)) permission management and volume creation and deletion


hdafs
----

Script for managing AFS permssions - setting or resetting directory permssions for a user

###SYNOPSIS###
      hdafs [-h] [-erRvV] [-s USER -p PERMISSION]

###DESCRIPTION###
      Set, reset, or examine AFS permissions
    
      -h  show this help text
      -e  examine existing permissions
      -r  apply permissions recursively
      -R  reset (wipe) existing permissions before applying (be careful!)
      -s  set the user(s) permissions (requires -p)
      -p  permissions
      -v  print the script version
        
      permissions:
          all    Full AFS permissions (rlidwka)
          write  Write permissions (rliwk)
          read   Read-only permissions (rl)
          none   No permissions

###Known Issues###

None reported

###Version###

This Readme.md file is up-to-date with hdafs version 1.1.

###AUTHOR###

Written by Chris Collins \<collins.christopher@gmail.com\>

Copyright Information
---------------------

Copyright (C) 2014 Chris Collins

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

