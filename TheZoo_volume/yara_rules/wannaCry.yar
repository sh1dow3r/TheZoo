/*
   YARA Rule Set
   Author: Wannacry
   Date: 2022-03-13
   Identifier: mal
   Reference: Wannacry
*/

/* Rule Set ----------------------------------------------------------------- */

rule wannacry {
   meta:
      description = "mal - file wannacry.bin"
      author = "Wannacry"
      reference = "Wannacry"
      date = "2022-03-13"
      hash1 = "32f24601153be0885f11d62e0a8a2f0280a2034fc981d8184180c5d3b1b9e8cf"
   strings:
      $x1 = "cmd.exe /c \"%s\"" fullword ascii
      $s2 = "msvcrtd.dll" fullword ascii
      $s3 = "launcher.dll" fullword ascii
      $s4 = "taskse.exe" fullword ascii
      $s5 = "taskdl.exe" fullword ascii
      $s6 = "tasksche.exe" fullword ascii
      $s7 = "mssecsvc.exe" fullword ascii
      $s8 = "http://www.ifferfsodp9ifjaposdfjhgosurijfaewrwergwea.com" fullword ascii
      $s9 = "Bftp1I3QdaPuJRmjwwsMVPRLNoZOvWtD9HteHBrxPFrR9U8VZkx2ZOf0cKEYCsVTYygtI1L8M85VxaaHPkYDa2y0r+Sfxdv2tfXIIhg18+wT/Q9D6zU5pyzNiVJnxOcS" ascii
      $s10 = "C:\\%s\\qeriuwjhrf" fullword ascii
      $s11 = "W7ued/BLAuVkbc8L5g5HkS6TStIYpkVM4KMl49iygRM841Xxoas4RZSesIE6Vi4TNYWLYtM/bbZ2O5kH6XwtgeTN7/eYA7tDOHraA9um6YO7MI2WqzViMpy1MdKiBVBs" ascii
      $s12 = "GySx4DGbmqS1LBX7zM4Mk9YmgeehLsqEYBHBHH1nG1qiehpuSriXaDarhzDiYd09u2z9A7mdMUrgj73sfY57/Js9MbgLOoyQDHoSTGYgL5oNKD2i404mzzPg6w/ayLDG" ascii
      $s13 = "h7RQJsZ/wFX9y28zvzY/rBKNi3Mrxgsjf2p7r0pCJMOaEL+mOdlPlbLWrpY5HNwTgEtw0rV3ARznLMA9AaxJKwF3nlRi3is3k6EaWnnfQmkVI6/vJk8fZNs005MECGxL" ascii
      $s14 = "RHKUDXyiU8whdEYNVyve1MAWt/TjSAZNVoLog3MEfx2qlXZFKZkmmBch01PeIpzevpf9xdsPItHzzgBLiyk2PVZG5eOOjiyo6DysGdE8JHCwqJidXARxJG1+9nybvRj5" ascii
      $s15 = "a7yIXXbWcSCdVZqK6xQ+eeFNiXs1f5rWd+4Qa/JJmGHTSERUATPC0YvfZFL831OivCuNl1eBGetCuavZrQO+1gsNWg2hLHCWVFPBloKkp3VFQ+YwuJv7CWC3qSmQkac5" ascii
   condition:
      uint16(0) == 0x5a4d and filesize < 11000KB and
      1 of ($x*) and 4 of them
}
