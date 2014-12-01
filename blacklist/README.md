blacklist.py
==============

_Version 0.5.1 - 20141201_

Script to grab [CIF-generated](https://code.google.com/p/collective-intelligence-framework/) list of IPs or IP+Subnet Mask from a URL and apply those rules to a "BLACKLIST" chain in IPTables

###SYNOPSIS###

    blacklist.py

This script takes no arguments.

###Known Issues###

1. Subprocess check if BLACKLIST chain exists MUST be assigned to something, or the whole thing bombs out.  I'm not sure why this is yet.  Work around so far was to assign stdout to an unused variable.

###Version###

This Readme.md file is up-to-date with blacklist.py Version 0.5.1

###AUTHOR###

Written by Chris Collins \<collins.christopher@gmail.com\>

Copyright Information
---------------------

Copyright (C) 2014 Chris Collins

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

