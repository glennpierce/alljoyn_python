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


# -*- coding: utf-8 -*-

import ctypes as C
from ctypes.util import find_library
import sys
from enum import Enum, unique

class Handle(C.c_void_p):
    pass

class BusAttachmentHandle(C.c_void_p):
    pass

class AboutDataHandle(C.c_void_p):
    pass

class AboutListenerHandle(C.c_void_p): 
    pass

class AboutObjectHandle(C.c_void_p):
    pass

class AboutProxyHandle(C.c_void_p): 
    pass

class BusListenerHandle(C.c_void_p):
    pass

class BusObjectHandle(C.c_void_p): 
    pass

class InterfaceDescriptionHandle(C.c_void_p):
    pass

class MessageHandle(C.c_void_p):
    pass

class MsgArgHandle(C.c_void_p): 
    pass

class ProxyBusHandle(C.c_void_p):
    pass

class SessionOptsHandle(C.c_void_p): 
    pass

class SessionListenerHandle(C.c_void_p):
    pass

class SessionPortListenerHandle(C.c_void_p): 
    pass

@unique
class QStatus(Enum):
    ER_OK = 0x0  # Success.
    ER_FAIL = 0x1  # Generic failure.
    ER_UTF_CONVERSION_FAILED = 0x2  # Conversion between UTF bases failed.
    ER_BUFFER_TOO_SMALL = 0x3  # Not enough space in buffer for operation.
    ER_OS_ERROR = 0x4  # Underlying OS has indicated an error.
    ER_OUT_OF_MEMORY = 0x5  # Failed to allocate memory.
    ER_SOCKET_BIND_ERROR = 0x6  # Bind to IP address failed.
    ER_INIT_FAILED = 0x7  # Initialization failed.
    ER_WOULDBLOCK = 0x8  # An I/O attempt on non-blocking resource would block
    ER_NOT_IMPLEMENTED = 0x9  # Feature not implemented
    ER_TIMEOUT = 0xa  # Operation timed out
    ER_SOCK_OTHER_END_CLOSED = 0xb  # Other end closed the socket
    ER_BAD_ARG_1 = 0xc  # Function call argument 1 is invalid
    ER_BAD_ARG_2 = 0xd  # Function call argument 2 is invalid
    ER_BAD_ARG_3 = 0xe  # Function call argument 3 is invalid
    ER_BAD_ARG_4 = 0xf  # Function call argument 4 is invalid
    ER_BAD_ARG_5 = 0x10  # Function call argument 5 is invalid
    ER_BAD_ARG_6 = 0x11  # Function call argument 6 is invalid
    ER_BAD_ARG_7 = 0x12  # Function call argument 7 is invalid
    ER_BAD_ARG_8 = 0x13  # Function call argument 8 is invalid
    ER_INVALID_ADDRESS = 0x14  # Address is NULL or invalid
    ER_INVALID_DATA = 0x15  # Generic invalid data error
    ER_READ_ERROR = 0x16  # Generic read error
    ER_WRITE_ERROR = 0x17  # Generic write error
    ER_OPEN_FAILED = 0x18  # Generic open failure
    ER_PARSE_ERROR = 0x19  # Generic parse failure
    ER_END_OF_DATA = 0x1A  # Generic EOD/EOF error
    ER_CONN_REFUSED = 0x1B  # Connection was refused because no one is listening
    ER_BAD_ARG_COUNT = 0x1C  # Incorrect number of arguments given to function call
    ER_WARNING = 0x1D  # Generic warning
    ER_EOF = 0x1E  # End of file
    ER_DEADLOCK = 0x1F  # Operation would cause deadlock
    ER_COMMON_ERRORS = 0x1000  # Error code block for the Common subsystem.
    ER_STOPPING_THREAD = 0x1001  # Operation interrupted by ERThread stop signal.
    ER_ALERTED_THREAD = 0x1002  # Operation interrupted by ERThread alert signal.
    ER_XML_MALFORMED = 0x1003  # Cannot parse malformed XML
    ER_AUTH_FAIL = 0x1004  # Authentication failed
    ER_AUTH_USER_REJECT = 0x1005  # Authentication was rejected by user
    ER_NO_SUCH_ALARM = 0x1006  # Attempt to reference non-existent timer alarm
    ER_TIMER_FALLBEHIND = 0x1007  # A timer thread is missing scheduled alarm times
    ER_SSL_ERRORS = 0x1008  # Error code block for SSL subsystem
    ER_SSL_INIT = 0x1009  # SSL initialization failed.
    ER_SSL_CONNECT = 0x100a  # Failed to connect to remote host using SSL
    ER_SSL_VERIFY = 0x100b  # Failed to verify identity of SSL destination
    ER_EXTERNAL_THREAD = 0x100c  # Operation not supported on external thread wrapper
    ER_CRYPTO_ERROR = 0x100d  # Non-specific error in the crypto subsystem
    ER_CRYPTO_TRUNCATED = 0x100e  # Not enough room for key
    ER_CRYPTO_KEY_UNAVAILABLE = 0x100f  # No key to return
    ER_BAD_HOSTNAME = 0x1010  # Cannot lookup hostname
    ER_CRYPTO_KEY_UNUSABLE = 0x1011  # Key cannot be used
    ER_EMPTY_KEY_BLOB = 0x1012  # Key blob is empty
    ER_CORRUPT_KEYBLOB = 0x1013  # Key blob is corrupted
    ER_INVALID_KEY_ENCODING = 0x1014  # Encoded key is not valid
    ER_DEAD_THREAD = 0x1015  # Operation not allowed thread is dead
    ER_THREAD_RUNNING = 0x1016  # Cannot start a thread that is already running
    ER_THREAD_STOPPING = 0x1017  # Cannot start a thread that is already stopping
    ER_BAD_STRING_ENCODING = 0x1018  # Encoded string did not have the expected format or contents
    ER_CRYPTO_INSUFFICIENT_SECURITY = 0x1019  # Crypto algorithm parameters do not provide sufficient security
    ER_CRYPTO_ILLEGAL_PARAMETERS = 0x101a  # Crypto algorithm parameter value is illegal
    ER_CRYPTO_HASH_UNINITIALIZED = 0x101b  # Cryptographic hash function must be initialized
    ER_THREAD_NO_WAIT = 0x101c  # Thread cannot be blocked by a WAIT or SLEEP call
    ER_TIMER_EXITING = 0x101d  # Cannot add an alarm to a timer that is exiting
    ER_INVALID_GUID = 0x101e  # String is not a hex encoded GUID string
    ER_THREADPOOL_EXHAUSTED = 0x101f  # A thread pool has reached its specified concurrency
    ER_THREADPOOL_STOPPING = 0x1020  # Cannot execute a closure on a stopping thread pool
    ER_INVALID_STREAM = 0x1021  # Attempt to reference non-existent stream entry
    ER_TIMER_FULL = 0x1022  # Attempt to reference non-existent stream entry
    # Cannot execute a read or write command on an IODispatch thread because it is stopping.
    ER_IODISPATCH_STOPPING = 0x1023
    ER_SLAP_INVALID_PACKET_LEN = 0x1024  # Length of SLAP packet is invalid.
    ER_SLAP_HDR_CHECKSUM_ERROR = 0x1025  # SLAP packet header checksum error.
    ER_SLAP_INVALID_PACKET_TYPE = 0x1026  # Invalid SLAP packet type.
    ER_SLAP_LEN_MISMATCH = 0x1027  # Calculated length does not match the received length.
    ER_SLAP_PACKET_TYPE_MISMATCH = 0x1028  # Packet type does not match reliability bit.
    ER_SLAP_CRC_ERROR = 0x1029  # SLAP packet CRC error.
    ER_SLAP_ERROR = 0x102A  # Generic SLAP error.
    ER_SLAP_OTHER_END_CLOSED = 0x102B  # Other end closed the SLAP connection
    ER_TIMER_NOT_ALLOWED = 0x102C  # Timer EnableReentrancy call not allowed
    ER_NONE = 0xffff  # No error code to report
    ER_BUS_ERRORS = 0x9000  # Error code block for ALLJOYN wire protocol
    ER_BUS_READ_ERROR = 0x9001  # Error attempting to read
    ER_BUS_WRITE_ERROR = 0x9002  # Error attempting to write
    ER_BUS_BAD_VALUE_TYPE = 0x9003  # Read an invalid value type
    ER_BUS_BAD_HEADER_FIELD = 0x9004  # Read an invalid header field
    ER_BUS_BAD_SIGNATURE = 0x9005  # Signature was badly formed
    ER_BUS_BAD_OBJ_PATH = 0x9006  # Object path contained an illegal character
    ER_BUS_BAD_MEMBER_NAME = 0x9007  # A member name contained an illegal character
    ER_BUS_BAD_INTERFACE_NAME = 0x9008  # An interface name contained an illegal character
    ER_BUS_BAD_ERROR_NAME = 0x9009  # An error name contained an illegal character
    ER_BUS_BAD_BUS_NAME = 0x900a  # A bus name contained an illegal character
    ER_BUS_NAME_TOO_LONG = 0x900b  # A name exceeded the permitted length
    ER_BUS_BAD_LENGTH = 0x900c  # Length of an array was not a multiple of the array element size
    ER_BUS_BAD_VALUE = 0x900d  # Parsed value in a message was invalid (for example: boolean > 1)
    ER_BUS_BAD_HDR_FLAGS = 0x900e  # Unknown header flags
    ER_BUS_BAD_BODY_LEN = 0x900f  # Body length was to long or too short
    ER_BUS_BAD_HEADER_LEN = 0x9010  # Header length was to long or too short
    ER_BUS_UNKNOWN_SERIAL = 0x9011  # Serial number in a method response was unknown
    ER_BUS_UNKNOWN_PATH = 0x9012  # Path in a method call or signal was unknown
    ER_BUS_UNKNOWN_INTERFACE = 0x9013  # Interface in a method call or signal was unknown
    ER_BUS_ESTABLISH_FAILED = 0x9014  # Failed to establish a connection
    ER_BUS_UNEXPECTED_SIGNATURE = 0x9015  # Signature in message was not what was expected
    ER_BUS_INTERFACE_MISSING = 0x9016  # Interface header field is missing
    ER_BUS_PATH_MISSING = 0x9017  # Object path header field is missing
    ER_BUS_MEMBER_MISSING = 0x9018  # Member header field is missing
    ER_BUS_REPLY_SERIAL_MISSING = 0x9019  # Reply-Serial header field is missing
    ER_BUS_ERROR_NAME_MISSING = 0x901a  # Error Name header field is missing
    ER_BUS_INTERFACE_NO_SUCH_MEMBER = 0x901b  # Interface does not have the requested member
    ER_BUS_NO_SUCH_OBJECT = 0x901c  # Object does not exist
    ER_BUS_OBJECT_NO_SUCH_MEMBER = 0x901d  # Object does not have the requested member (on any interface)
    ER_BUS_OBJECT_NO_SUCH_INTERFACE = 0x901e  # Object does not have the requested interface
    ER_BUS_NO_SUCH_INTERFACE = 0x901f  # Requested interface does not exist
    ER_BUS_MEMBER_NO_SUCH_SIGNATURE = 0x9020  # Member exists but does not have the requested signature
    ER_BUS_NOT_NUL_TERMINATED = 0x9021  # A string or signature was not NUL terminated
    ER_BUS_NO_SUCH_PROPERTY = 0x9022  # No such property for a GET or SET operation
    ER_BUS_SET_WRONG_SIGNATURE = 0x9023  # Attempt to set a property value with the wrong signature
    ER_BUS_PROPERTY_VALUE_NOT_SET = 0x9024  # Attempt to get a property whose value has not been set
    ER_BUS_PROPERTY_ACCESS_DENIED = 0x9025  # Attempt to set or get a property failed due to access rights
    ER_BUS_NO_TRANSPORTS = 0x9026  # No physical message transports were specified
    ER_BUS_BAD_TRANSPORT_ARGS = 0x9027  # Missing or badly formatted transports args specified
    ER_BUS_NO_ROUTE = 0x9028  # Message cannot be routed to destination
    ER_BUS_NO_ENDPOINT = 0x9029  # An endpoint with given name cannot be found
    ER_BUS_BAD_SEND_PARAMETER = 0x902a  # Bad parameter in send message call
    ER_BUS_UNMATCHED_REPLY_SERIAL = 0x902b  # Serial number in method call reply message did not match any method calls
    ER_BUS_BAD_SENDER_ID = 0x902c  # Sender identifier is invalid
    ER_BUS_TRANSPORT_NOT_STARTED = 0x902d  # Attempt to send on a transport that has not been started
    ER_BUS_EMPTY_MESSAGE = 0x902e  # Attempt to deliver an empty message
    ER_BUS_NOT_OWNER = 0x902f  # A bus name operation was not permitted because sender does not own name
    ER_BUS_SET_PROPERTY_REJECTED = 0x9030  # Application rejected a request to set a property
    ER_BUS_CONNECT_FAILED = 0x9031  # Connection failed
    ER_BUS_REPLY_IS_ERROR_MESSAGE = 0x9032  # Response from a method call was an ERROR message
    ER_BUS_NOT_AUTHENTICATING = 0x9033  # Not in an authentication conversation
    ER_BUS_NO_LISTENER = 0x9034  # A listener is required to implement the requested function
    ER_BUS_NOT_ALLOWED = 0x9036  # The operation attempted is not allowed
    ER_BUS_WRITE_QUEUE_FULL = 0x9037  # Write failed because write queue is full
    ER_BUS_ENDPOINT_CLOSING = 0x9038  # Operation not permitted on endpoint in process of closing
    ER_BUS_INTERFACE_MISMATCH = 0x9039  # Received two conflicting definitions for the same interface
    ER_BUS_MEMBER_ALREADY_EXISTS = 0x903a  # Attempt to add a member to an interface that already exists
    ER_BUS_PROPERTY_ALREADY_EXISTS = 0x903b  # Attempt to add a property to an interface that already exists
    ER_BUS_IFACE_ALREADY_EXISTS = 0x903c  # Attempt to add an interface to an object that already exists
    ER_BUS_ERROR_RESPONSE = 0x903d  # Received an error response to a method call
    ER_BUS_BAD_XML = 0x903e  # XML data is improperly formatted
    ER_BUS_BAD_CHILD_PATH = 0x903f  # The path of a child object is incorrect given its parent's path
    ER_BUS_OBJ_ALREADY_EXISTS = 0x9040  # Attempt to add a RemoteObject child that already exists
    ER_BUS_OBJ_NOT_FOUND = 0x9041  # Object with given path does not exist
    ER_BUS_CANNOT_EXPAND_MESSAGE = 0x9042  # Expansion information for a compressed message is not available
    ER_BUS_NOT_COMPRESSED = 0x9043  # Attempt to expand a message that is not compressed
    ER_BUS_ALREADY_CONNECTED = 0x9044  # Attempt to connect to a bus which is already connected
    ER_BUS_NOT_CONNECTED = 0x9045  # Attempt to use a bus attachment that is not connected to a router
    ER_BUS_ALREADY_LISTENING = 0x9046  # Attempt to listen on a bus address which is already being listened on
    ER_BUS_KEY_UNAVAILABLE = 0x9047  # The request key is not available
    ER_BUS_TRUNCATED = 0x9048  # Insufficient memory to copy data
    ER_BUS_KEY_STORE_NOT_LOADED = 0x9049  # Accessing the key store before it is loaded
    ER_BUS_NO_AUTHENTICATION_MECHANISM = 0x904a  # There is no authentication mechanism
    ER_BUS_BUS_ALREADY_STARTED = 0x904b  # Bus has already been started
    ER_BUS_BUS_NOT_STARTED = 0x904c  # Bus has not yet been started
    ER_BUS_KEYBLOB_OP_INVALID = 0x904d  # The operation requested cannot be performed using this key blob
    ER_BUS_INVALID_HEADER_CHECKSUM = 0x904e  # Invalid header checksum in an encrypted message
    ER_BUS_MESSAGE_NOT_ENCRYPTED = 0x904f  # Security policy requires the message to be encrypted
    ER_BUS_INVALID_HEADER_SERIAL = 0x9050  # Serial number in message header is invalid
    ER_BUS_TIME_TO_LIVE_EXPIRED = 0x9051  # Message time-to-live has expired
    ER_BUS_HDR_EXPANSION_INVALID = 0x9052  # Something is wrong with a header expansion
    ER_BUS_MISSING_COMPRESSION_TOKEN = 0x9053  # Compressed headers require a compression token
    ER_BUS_NO_PEER_GUID = 0x9054  # There is no GUID for this peer
    ER_BUS_MESSAGE_DECRYPTION_FAILED = 0x9055  # Message decryption failed
    ER_BUS_SECURITY_FATAL = 0x9056  # A fatal security failure
    ER_BUS_KEY_EXPIRED = 0x9057  # An encryption key has expired
    ER_BUS_CORRUPT_KEYSTORE = 0x9058  # Key store is corrupt
    ER_BUS_NO_CALL_FOR_REPLY = 0x9059  # A reply only allowed in response to a method call
    ER_BUS_NOT_A_COMPLETE_TYPE = 0x905a  # Signature must be a single complete type
    ER_BUS_POLICY_VIOLATION = 0x905b  # Message does not meet policy restrictions
    ER_BUS_NO_SUCH_SERVICE = 0x905c  # Service name is unknown
    ER_BUS_TRANSPORT_NOT_AVAILABLE = 0x905d  # Transport cannot be used due to underlying mechanism disabled by OS
    ER_BUS_INVALID_AUTH_MECHANISM = 0x905e  # Authentication mechanism is not valid
    ER_BUS_KEYSTORE_VERSION_MISMATCH = 0x905f  # Key store has wrong version number
    ER_BUS_BLOCKING_CALL_NOT_ALLOWED = 0x9060  # A synchronous method call from within handler is not permitted.
    ER_BUS_SIGNATURE_MISMATCH = 0x9061  # MsgArg(s) do not match signature.
    ER_BUS_STOPPING = 0x9062  # The bus is stopping.
    ER_BUS_METHOD_CALL_ABORTED = 0x9063  # The method call was aborted.
    ER_BUS_CANNOT_ADD_INTERFACE = 0x9064  # An interface cannot be added to an object that is already registered.
    ER_BUS_CANNOT_ADD_HANDLER = 0x9065  # A method handler cannot be added to an object that is already registered.
    ER_BUS_KEYSTORE_NOT_LOADED = 0x9066  # Key store has not been loaded
    ER_BUS_NO_SUCH_HANDLE = 0x906b  # Handle is not in the handle table
    ER_BUS_HANDLES_NOT_ENABLED = 0x906c  # Passing of handles is not enabled for this connection
    ER_BUS_HANDLES_MISMATCH = 0x906d  # Message had more handles than expected
    ER_BUS_NO_SESSION = 0x906f  # Session id is not valid
    ER_BUS_ELEMENT_NOT_FOUND = 0x9070  # Dictionary element was not found
    ER_BUS_NOT_A_DICTIONARY = 0x9071  # MsgArg was not an array of dictionary elements
    ER_BUS_WAIT_FAILED = 0x9072  # Wait failed
    ER_BUS_BAD_SESSION_OPTS = 0x9074  # Session options are bad or incompatible
    ER_BUS_CONNECTION_REJECTED = 0x9075  # Incoming connection rejected
    ER_DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER = 0x9076  # RequestName reply: Name was successfully obtained
    # RequestName reply: Name is already owned, request for name has been queued
    ER_DBUS_REQUEST_NAME_REPLY_IN_QUEUE = 0x9077
    # RequestName reply: Name is already owned and DO_NOT_QUEUE was specified in request
    ER_DBUS_REQUEST_NAME_REPLY_EXISTS = 0x9078
    ER_DBUS_REQUEST_NAME_REPLY_ALREADY_OWNER = 0x9079  # RequestName reply: Name is already owned by this endpoint
    ER_DBUS_RELEASE_NAME_REPLY_RELEASED = 0x907a  # ReleaseName reply: Name was released
    ER_DBUS_RELEASE_NAME_REPLY_NON_EXISTENT = 0x907b  # ReleaseName reply: Name does not exist
    # ReleaseName reply: Request to release name that is not owned by this endpoint
    ER_DBUS_RELEASE_NAME_REPLY_NOT_OWNER = 0x907c
    ER_DBUS_START_REPLY_ALREADY_RUNNING = 0x907e  # StartServiceByName reply: Service is already running
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_ALREADY_EXISTS = 0x9080  # BindSessionPort reply: SessionPort already exists
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_FAILED = 0x9081  # BindSessionPort reply: Failed
    ER_ALLJOYN_JOINSESSION_REPLY_NO_SESSION = 0x9083  # JoinSession reply: Session with given name does not exist
    ER_ALLJOYN_JOINSESSION_REPLY_UNREACHABLE = 0x9084  # JoinSession reply: Failed to find suitable transport
    ER_ALLJOYN_JOINSESSION_REPLY_CONNECT_FAILED = 0x9085  # JoinSession reply: Connect to advertised address
    ER_ALLJOYN_JOINSESSION_REPLY_REJECTED = 0x9086  # JoinSession reply: The session creator rejected the join req
    # JoinSession reply: Failed due to session option incompatibilities
    ER_ALLJOYN_JOINSESSION_REPLY_BAD_SESSION_OPTS = 0x9087
    ER_ALLJOYN_JOINSESSION_REPLY_FAILED = 0x9088  # JoinSession reply: Failed for unknown reason
    ER_ALLJOYN_LEAVESESSION_REPLY_NO_SESSION = 0x908a  # LeaveSession reply: Session with given name does not exist
    ER_ALLJOYN_LEAVESESSION_REPLY_FAILED = 0x908b  # LeaveSession reply: Failed for unspecified reason
    # AdvertiseName reply: The specified transport is unavailable for advertising
    ER_ALLJOYN_ADVERTISENAME_REPLY_TRANSPORT_NOT_AVAILABLE = 0x908c
    # AdvertiseName reply: This endpoint is already advertising this name
    ER_ALLJOYN_ADVERTISENAME_REPLY_ALREADY_ADVERTISING = 0x908d
    ER_ALLJOYN_ADVERTISENAME_REPLY_FAILED = 0x908e  # AdvertiseName reply: Advertise failed
    ER_ALLJOYN_CANCELADVERTISENAME_REPLY_FAILED = 0x9090  # CancelAdvertiseName reply: Advertise failed
    # FindAdvertisedName reply: The specified transport is unavailable for discovery
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_TRANSPORT_NOT_AVAILABLE = 0x9091
    # FindAdvertisedName reply: This endpoint is already discovering this name
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_ALREADY_DISCOVERING = 0x9092
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_FAILED = 0x9093  # FindAdvertisedName reply: Failed
    ER_ALLJOYN_CANCELFINDADVERTISEDNAME_REPLY_FAILED = 0x9095  # CancelFindAdvertisedName reply: Failed
    ER_BUS_UNEXPECTED_DISPOSITION = 0x9096  # An unexpected disposition was returned and has been treated as an error
    ER_BUS_INTERFACE_ACTIVATED = 0x9097  # An InterfaceDescription cannot be modified once activated
    ER_ALLJOYN_UNBINDSESSIONPORT_REPLY_BAD_PORT = 0x9098  # UnbindSessionPort reply: SessionPort does not exist
    ER_ALLJOYN_UNBINDSESSIONPORT_REPLY_FAILED = 0x9099  # UnbindSessionPort reply: Failed
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_INVALID_OPTS = 0x909a  # BindSessionPort reply: SessionOpts are invalid
    ER_ALLJOYN_JOINSESSION_REPLY_ALREADY_JOINED = 0x909b  # JoinSession reply: Caller has already joined the session
    ER_BUS_SELF_CONNECT = 0x909c  # Received BusHello from self
    ER_BUS_SECURITY_NOT_ENABLED = 0x909d  # Security is not enabled for this bus attachment
    ER_BUS_LISTENER_ALREADY_SET = 0x909e  # A listener has already been set
    ER_BUS_PEER_AUTH_VERSION_MISMATCH = 0x909f  # Incompatible peer authentication version numbers
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_NOT_SUPPORTED = 0x90a0  # Local router does not support SetLinkTimeout
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_NO_DEST_SUPPORT = 0x90a1  # SetLinkTimeout not supported by destination
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_FAILED = 0x90a2  # SetLinkTimeout failed
    ER_ALLJOYN_ACCESS_PERMISSION_WARNING = 0x90a3  # No permission to use Wifi
    ER_ALLJOYN_ACCESS_PERMISSION_ERROR = 0x90a4  # No permission to access peer service
    ER_BUS_DESTINATION_NOT_AUTHENTICATED = 0x90a5  # Cannot send a signal to a destination that is not authenticated
    ER_BUS_ENDPOINT_REDIRECTED = 0x90a6  # Endpoint was redirected to another address
    ER_BUS_AUTHENTICATION_PENDING = 0x90a7  # Authentication of remote peer is pending
    ER_BUS_NOT_AUTHORIZED = 0x90a8  # Operation was not authorized
    ER_PACKET_BUS_NO_SUCH_CHANNEL = 0x90a9  # Received packet for unknown channel
    ER_PACKET_BAD_FORMAT = 0x90aa  # Received packet with incorrect header information
    ER_PACKET_CONNECT_TIMEOUT = 0x90ab  # Timed out waiting for connect response
    ER_PACKET_CHANNEL_FAIL = 0x90ac  # Failed to create new comm channel
    ER_PACKET_TOO_LARGE = 0x90ad  # Message too large for use with packet based transport
    ER_PACKET_BAD_PARAMETER = 0x90ae  # Invalid PacketEngine control packet received
    ER_PACKET_BAD_CRC = 0x90af  # Packet has invalid CRC
    # Rendezvous Server has deactivated the current user. Register with the Rendezvous Server to continue.
    ER_RENDEZVOUS_SERVER_DEACTIVATED_USER = 0x90cb
    # Rendezvous Server does not recognize the current user. Register with the Rendezvous Server to continue.
    ER_RENDEZVOUS_SERVER_UNKNOWN_USER = 0x90cc
    ER_UNABLE_TO_CONNECT_TO_RENDEZVOUS_SERVER = 0x90cd  # Unable to connect to the Rendezvous Server
    ER_NOT_CONNECTED_TO_RENDEZVOUS_SERVER = 0x90ce  # Not connected to the Rendezvous Server
    ER_UNABLE_TO_SEND_MESSAGE_TO_RENDEZVOUS_SERVER = 0x90cf  # Unable to send message to the Rendezvous Server
    ER_INVALID_RENDEZVOUS_SERVER_INTERFACE_MESSAGE = 0x90d0  # Invalid Rendezvous Server interface message
    # Invalid message response received over the Persistent connection with the Rendezvous Server
    ER_INVALID_PERSISTENT_CONNECTION_MESSAGE_RESPONSE = 0x90d1
    # Invalid message response received over the On Demand connection with the Rendezvous Server
    ER_INVALID_ON_DEMAND_CONNECTION_MESSAGE_RESPONSE = 0x90d2
    # Invalid HTTP method type used for Rendezvous Server interface message
    ER_INVALID_HTTP_METHOD_USED_FOR_RENDEZVOUS_SERVER_INTERFACE_MESSAGE = 0x90d3
    # Received a HTTP 500 status code from the Rendezvous Server. This indicates an internal error in the Server
    ER_RENDEZVOUS_SERVER_ERR500_INTERNAL_ERROR = 0x90d4
    # Received a HTTP 503 status code from the Rendezvous Server. This
    # indicates unavailability of the Server error state
    ER_RENDEZVOUS_SERVER_ERR503_STATUS_UNAVAILABLE = 0x90d5
    # Received a HTTP 401 status code from the Rendezvous Server. This
    # indicates that the client is unauthorized to send a request to the
    # Server. The Client login procedure must be initiated.
    ER_RENDEZVOUS_SERVER_ERR401_UNAUTHORIZED_REQUEST = 0x90d6
    # Received a HTTP status code indicating unrecoverable error from the
    # Rendezvous Server. The connection with the Server should be
    # re-established.
    ER_RENDEZVOUS_SERVER_UNRECOVERABLE_ERROR = 0x90d7
    ER_RENDEZVOUS_SERVER_ROOT_CERTIFICATE_UNINITIALIZED = 0x90d8  # Rendezvous Server root ceritificate uninitialized.
    ER_BUS_NO_SUCH_ANNOTATION = 0x90d9  # No such annotation for a GET or SET operation
    # Attempt to add an annotation to an interface or property that already exists
    ER_BUS_ANNOTATION_ALREADY_EXISTS = 0x90da
    ER_SOCK_CLOSING = 0x90db  # Socket close in progress
    ER_NO_SUCH_DEVICE = 0x90dc  # A referenced device cannot be located
    ER_P2P = 0x90dd  # An error occurred in a Wi-Fi Direct helper method call
    ER_P2P_TIMEOUT = 0x90de  # A timeout occurred in a Wi-Fi Direct helper method call
    ER_P2P_NOT_CONNECTED = 0x90df  # A required Wi-Fi Direct network connection does not exist
    ER_BAD_TRANSPORT_MASK = 0x90e0  # Exactly one mask bit was not set in the provided TransportMask
    ER_PROXIMITY_CONNECTION_ESTABLISH_FAIL = 0x90e1  # Fail to establish P2P proximity connection
    ER_PROXIMITY_NO_PEERS_FOUND = 0x90e2  # Cannot find proximity P2P peers
    ER_BUS_OBJECT_NOT_REGISTERED = 0x90e3  # Operation not permitted on unregistered bus object
    ER_P2P_DISABLED = 0x90e4  # Wi-Fi Direct is disabled on the device
    ER_P2P_BUSY = 0x90e5  # Wi-Fi Direct resources are in busy state
    ER_BUS_INCOMPATIBLE_DAEMON = 0x90e6  # The router version is too old to be used by this client
    ER_P2P_NO_GO = 0x90e7  # Attempt to execute a Wi-Fi Direct GO-related operation while STA
    ER_P2P_NO_STA = 0x90e8  # Attempt to execute a Wi-Fi Direct STA-related operation while GO
    ER_P2P_FORBIDDEN = 0x90e9  # Attempt to execute a forbidden Wi-Fi Direct operation
    ER_ALLJOYN_ONAPPSUSPEND_REPLY_FAILED = 0x90ea  # OnAppSuspend reply: Failed
    ER_ALLJOYN_ONAPPSUSPEND_REPLY_UNSUPPORTED = 0x90eb  # OnAppSuspend reply: Unsupported operation
    ER_ALLJOYN_ONAPPRESUME_REPLY_FAILED = 0x90ec  # OnAppResume reply: Failed
    ER_ALLJOYN_ONAPPRESUME_REPLY_UNSUPPORTED = 0x90ed  # OnAppResume reply: Unsupported operation
    ER_BUS_NO_SUCH_MESSAGE = 0x90ee  # Message not found
    # RemoveSessionMember reply: Specified session Id with this endpoint was not found
    ER_ALLJOYN_REMOVESESSIONMEMBER_REPLY_NO_SESSION = 0x90ef
    # RemoveSessionMember reply: Endpoint is not the binder of session
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_BINDER = 0x90f0
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_MULTIPOINT = 0x90f1  # RemoveSessionMember reply: Session is not multipoint
    # RemoveSessionMember reply: Specified session member was not found
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_FOUND = 0x90f2
    # RemoveSessionMember reply: The remote router does not support this feature
    ER_ALLJOYN_REMOVESESSIONMEMBER_INCOMPATIBLE_REMOTE_DAEMON = 0x90f3
    ER_ALLJOYN_REMOVESESSIONMEMBER_REPLY_FAILED = 0x90f4  # RemoveSessionMember reply: Failed for unspecified reason
    ER_BUS_REMOVED_BY_BINDER = 0x90f5  # The session member was removed by the binder
    ER_BUS_MATCH_RULE_NOT_FOUND = 0x90f6  # The match rule was not found
    ER_ALLJOYN_PING_FAILED = 0x90f7  # Ping failed
    ER_ALLJOYN_PING_REPLY_UNREACHABLE = 0x90f8  # Name pinged is unreachable
    ER_UDP_MSG_TOO_LONG = 0x90f9  # The message is too long to transmit over the UDP transport
    ER_UDP_DEMUX_NO_ENDPOINT = 0x90fa  # Tried to demux the callback but found no endpoint for the connection
    ER_UDP_NO_NETWORK = 0x90fb  # Not listening on network implied by IP address
    ER_UDP_UNEXPECTED_LENGTH = 0x90fc  # Request for more bytes than are in the underlying datagram
    ER_UDP_UNEXPECTED_FLOW = 0x90fd  # The data flow type of the endpoint has an unexpected value
    ER_UDP_DISCONNECT = 0x90fe  # Unexpected disconnect occurred
    ER_UDP_NOT_IMPLEMENTED = 0x90ff  # Feature not implemented for the UDP transport
    ER_UDP_NO_LISTENER = 0x9100  # Discovery started with no listener to receive callbacks
    ER_UDP_STOPPING = 0x9101  # Attempt to use UDP when transport stopping
    ER_ARDP_BACKPRESSURE = 0x9102  # ARDP is applying backpressure -- send window is full
    ER_UDP_BACKPRESSURE = 0x9103  # UDP is applying backpressure to ARDP -- queue is full
    ER_ARDP_INVALID_STATE = 0x9104  # Current ARDP state does not allow attempted operation
    ER_ARDP_TTL_EXPIRED = 0x9105  # Time-To-Live of ARDP segment has expired
    ER_ARDP_PERSIST_TIMEOUT = 0x9106  # Remote endpoint stopped consuming data -- send window is full
    ER_ARDP_PROBE_TIMEOUT = 0x9107  # ARDP link timeout
    ER_ARDP_REMOTE_CONNECTION_RESET = 0x9108  # Remote endpoint disconected: sent RST
    ER_UDP_BUSHELLO = 0x9109  # UDP Transport is unable to complete an operation relating to a BusHello Message
    ER_UDP_MESSAGE = 0x910a  # UDP Transport is unable to complete an operation on an AllJoyn Message
    ER_UDP_INVALID = 0x910b  # UDP Transport detected invalid data or parameters from network
    ER_UDP_UNSUPPORTED = 0x910c  # UDP Transport does not support the indicated operation or type
    ER_UDP_ENDPOINT_STALLED = 0x910d  # UDP Transport has detected an endpoint that is not terminating correctly
    ER_ARDP_INVALID_RESPONSE = 0x910e  # ARDP Transport detected invalid message data that causes disconnect
    ER_ARDP_INVALID_CONNECTION = 0x910f  # ARDP connection not found
    ER_UDP_LOCAL_DISCONNECT = 0x9110  # UDP Transport connection (intentionally) disconnected on local side
    ER_UDP_EARLY_EXIT = 0x9111  # UDP Transport connection aborted during setup
    ER_UDP_LOCAL_DISCONNECT_FAIL = 0x9112  # UDP Transport local connection disconnect failure
    ER_ARDP_DISCONNECTING = 0x9113  # ARDP connection is being shut down
    ER_ALLJOYN_PING_REPLY_INCOMPATIBLE_REMOTE_ROUTING_NODE = 0x9114  # Remote routing node does not implement Ping
    ER_ALLJOYN_PING_REPLY_TIMEOUT = 0x9115  # Ping call timeout
    ER_ALLJOYN_PING_REPLY_UNKNOWN_NAME = 0x9116  # Name not found currently or part of any known session
    ER_ALLJOYN_PING_REPLY_FAILED = 0x9117  # Generic Ping call error
    ER_TCP_MAX_UNTRUSTED = 0x9118  # The maximum configured number of Thin Library connections has been reached
    ER_ALLJOYN_PING_REPLY_IN_PROGRESS = 0x9119  # A ping request for same name is already in progress
    ER_LANGUAGE_NOT_SUPPORTED = 0x911a  # The language requested is not supported
    ER_ABOUT_FIELD_ALREADY_SPECIFIED = 0x911b  # A field using the same name is already specified.
    ER_UDP_NOT_DISCONNECTED = 0x911c  # A UDP stream was found to be connected during teardown
    ER_UDP_ENDPOINT_NOT_STARTED = 0x911d  # Attempt to send on a UDP endpoint that is not started
    ER_UDP_ENDPOINT_REMOVED = 0x911e  # Attempt to send on a UDP endpoint that has been removed
    ER_ARDP_VERSION_NOT_SUPPORTED = 0x911f  # Specified version of ARDP Protocol is not supported
    ER_CONNECTION_LIMIT_EXCEEDED = 0x9120  # Connection rejected due to configured connection limits
    ER_ARDP_WRITE_BLOCKED = 0x9121  # ARDP cannot write to UDP socket (queue is full)
    ER_PERMISSION_DENIED = 0x9122  # Permission denied
    # Default language must be specified before setting a localized field
    ER_ABOUT_DEFAULT_LANGUAGE_NOT_SPECIFIED = 0x9123
    ER_ABOUT_SESSIONPORT_NOT_BOUND = 0x9124  # Unable to announce session port that is not bound to the BusAttachment
    ER_ABOUT_ABOUTDATA_MISSING_REQUIRED_FIELD = 0x9125  # The AboutData is missing a required field.
    # The AboutDataListener returns invalid data. Most likely cause: the
    # announced data does not match with non-announced data.
    ER_ABOUT_INVALID_ABOUTDATA_LISTENER = 0x9126
    ER_BUS_PING_GROUP_NOT_FOUND = 0x9127  # Ping group did not exist
    ER_BUS_REMOVED_BY_BINDER_SELF = 0x9128  # The self-joined session member was removed by the binder
    ER_INVALID_CONFIG = 0x9129  # Invalid configuration item or combination of items detected
    # General error indicating the value given for an About Data field is invalid.
    ER_ABOUT_INVALID_ABOUTDATA_FIELD_VALUE = 0x912a
    # Error indicating the AppId field is not a 128-bit bite array.
    ER_ABOUT_INVALID_ABOUTDATA_FIELD_APPID_SIZE = 0x912b
    # The transport denied the connection attempt because the application doesn't have the required permissions.
    ER_BUS_TRANSPORT_ACCESS_DENIED = 0x912c
    ER_INVALID_CERTIFICATE = 0x912d  # Invalid certificate
    ER_CERTIFICATE_NOT_FOUND = 0x912e  # Certificate not found
    ER_DUPLICATE_CERTIFICATE = 0x912f  # Duplicate Certificate found
    ER_UNKNOWN_CERTIFICATE = 0x9130  # Unknown Certificate
    ER_MISSING_DIGEST_IN_CERTIFICATE = 0x9131  # Missing digest in certificate
    ER_DIGEST_MISMATCH = 0x9132  # Digest mismatch
    ER_DUPLICATE_KEY = 0x9133  # Duplicate key found
    ER_NO_COMMON_TRUST = 0x9134  # No common trust anchor found
    ER_MANIFEST_NOT_FOUND = 0x9135  # Permission manifest not found
    ER_INVALID_CERT_CHAIN = 0x9136  # Invalid certificate chain
    ER_NO_TRUST_ANCHOR = 0x9137  # No trust anchor
    ER_INVALID_APPLICATION_STATE = 0x9138  # Invalid application state
    ER_FEATURE_NOT_AVAILABLE = 0x9139  # Feature is not available
    ER_KEY_STORE_ALREADY_INITIALIZED = 0x913a  # Key store is already initialized
    ER_KEY_STORE_ID_NOT_YET_SET = 0x913b  # Key store ID is not yet set
    ER_POLICY_NOT_NEWER = 0x913c  # Installing permission policy not newer than existing policy
    ER_MANIFEST_REJECTED = 0x913d  # The manifest of the application was rejected.
    ER_INVALID_CERTIFICATE_USAGE = 0x913e  # The certificate extended key usage is not Alljoyn specific.
    ER_INVALID_SIGNAL_EMISSION_TYPE = 0x913f  # Attempt to send a signal with the wrong type. */


class AllJoynException(Exception):

    def __init__(self, message,):
        # Call the base class constructor with the parameters it needs
        super(AllJoynException, self).__init__(message)
       

class QStatusException(Exception):

    def __init__(self, message, qstatus):
        # Call the base class constructor with the parameters it needs
        super(QStatusException, self).__init__(message)
        self.QStatus = qstatus


class AllJoynMeta(type):

    def __new__(meta, name, bases, attrs):
        return super(AllJoynMeta, meta).__new__(meta, name, bases, attrs)


class AllJoynObject(object):

    if sys.platform == 'win32':
        functForLoad = C.windll
    else:
        functForLoad = C.cdll

    libName = find_library("liballjoyn_c.so")

    if sys.platform.startswith("darwin"):
        # on darwin load the lib with the normal LoadLibrary function.
        _lib = functForLoad.LoadLibrary(libName)
    else:
        # on the other systems, get the library like an attribute of the load function (ctypes.windll or ctypes.cdll)
        #self.lib = getattr(functForLoad, "/usr/lib64/" + libName)
        _lib = getattr(functForLoad, "liballjoyn_c.so")

    def __init__(self):
        pass

    @staticmethod
    def QStatusToException(status):
        qstatus = QStatus(status)
        if qstatus != QStatus.ER_OK:
            AllJoynObject._lib.QCC_StatusText.restype = C.c_char_p
            AllJoynObject._lib.QCC_StatusText.argtypes = [C.c_uint32]
            text = AllJoynObject._lib.QCC_StatusText(status)
            raise QStatusException(text, status)
        return qstatus

    @staticmethod
    def Boolean(result):
        return int(result)

    @classmethod
    def bind_functions_to_cls(cls):
        for callable_name, method in cls._cmethods.items():
            lib_function_name = method[0]
            return_name = method[1][0]
            args = []
            try:
                return_type = (method[1][1]) if method[1][1] else None
                args = method[2]
            except:
                print callable_name
                print method[1][1]
                raise

            cargs = []
            try:
                cargs = [a[1] for a in args if a]
            except:
                print args
                raise

            cmethod = getattr(AllJoynObject._lib, lib_function_name)

            if callable_name == "EnableConcurrentCallBacks":
                print "return_type", return_type

            if return_type:
                try:
                    cmethod.restype = AllJoynObject.QStatusToException if return_name == 'QStatus' else return_type
                except:
                    print callable_name
                    raise
            else:
                cmethod.restype = None

            if cargs:
                try:
                    cmethod.argtypes = cargs
                except:
                    print callable_name
                    raise

            if callable_name == "EnableConcurrentCallBacks":
                print callable_name, "cmethod.restype", cmethod.restype, "cmethod.argtypes", cmethod.argtypes

            setattr(cls, '_' + callable_name, cmethod)


import Init
import Version
import BusAttachment
#import AboutData
#import AboutListener
#import MsgArg


class AllJoyn(object):

    # def BusAttachment(self, application_name, allow_remote_mesages=True):
    #    from BusAttachment import BusAttachment
    #    return BusAttachment(application_name, allow_remote_mesages=True)

    @property
    def Version(self):
        return Version._GetVersion()

    @property
    def BuildInfo(self):
        return Version._GetBuildInfo()

    @property
    def BusAttachment(self):
        return BusAttachment

    def __init__(self):
        Init._Init()

    def __del__(self):
        Init._Shutdown()
