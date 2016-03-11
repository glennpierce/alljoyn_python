# Copyright Glenn Pierce. All rights reserved.
#
#    Permission to use, copy, modify, and/or distribute this software for any
#    purpose with or without fee is hereby granted, provided that the above
#    copyright notice and this permission notice appear in all copies.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

    
# Wrapper for file TransportMask.h

ALLJOYN_TRANSPORT_NONE = 0x0000   # no transports
ALLJOYN_TRANSPORT_LOCAL = 0x0001   # Local (same device) transport
ALLJOYN_TRANSPORT_TCP = 0x0004   # TCP/IP transport
ALLJOYN_TRANSPORT_UDP = 0x0100   # UDP/IP transport
ALLJOYN_TRANSPORT_EXPERIMENTAL = 0x8000   # Placeholder for expermimental transports
ALLJOYN_TRANSPORT_IP = (ALLJOYN_TRANSPORT_TCP | ALLJOYN_TRANSPORT_UDP)  # Any IP-based transport
ALLJOYN_TRANSPORT_ANY = (ALLJOYN_TRANSPORT_LOCAL | ALLJOYN_TRANSPORT_IP)  # ANY non-experimental transport
ALLJOYN_TRANSPORT_BLUETOOTH = ('attempted_use_of_deprecated_definition', 0x0002)   # Bluetooth transport
ALLJOYN_TRANSPORT_WLAN = ('attempted_use_of_deprecated_definition', 0x0004)   # Wireless local-area network transport
ALLJOYN_TRANSPORT_WWAN = ('attempted_use_of_deprecated_definition', 0x0008)   # Wireless wide-area network transport
ALLJOYN_TRANSPORT_LAN = ('attempted_use_of_deprecated_definition', 0x0010)   # Wired local-area network transport
# Transport using WinRT Proximity Framework
ALLJOYN_TRANSPORT_PROXIMITY = ('attempted_use_of_deprecated_definition', 0x0040)
ALLJOYN_TRANSPORT_WFD = ('attempted_use_of_deprecated_definition', 0x0080)   # Transport using Wi-Fi Direct transport
